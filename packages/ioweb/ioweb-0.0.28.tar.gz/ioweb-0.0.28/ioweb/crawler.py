import time
import sys
import logging
from threading import Event, Thread, Lock
from queue import Queue, PriorityQueue, Empty, Full
from urllib.parse import urlsplit 
import re
#import json
from bson import json_util as json
from urllib.request import urlopen
from traceback import format_exception
from collections import defaultdict
import gc
from copy import deepcopy, copy
from datetime import datetime
from uuid import uuid4

from .util import Pause, debug
#from .loop import MultiCurlLoop
from .network_service import NetworkService
from .stat import Stat
from .request import Request, CallbackRequest, BaseRequest
from .error import (
    get_error_tag, collect_error_context, DataNotValid,
    IowebConfigError
)
from .error_logger import ErrorLogger
from .proxylist import ProxyList


class Crawler(object):
    _taskgen_sleep_time = 0.01
    dataop_threshold_default = {
        'number': 500,
        'size': None,
        #'time': None,
    }
    dataop_threshold = {}
    network_service_class = NetworkService

    def task_generator(self):
        if False:
            yield None

    def __init__(self,
            network_threads=3,
            result_workers=4,
            num_task_generators=1,
            retry_limit=3,
            extra_data=None,
            stop_on_handler_error=False,
            debug=False,
            stat_logging=True,
            stat_logging_format='text',
            master_taskq=None
        ):
        self.uuid = uuid4().hex
        logging.debug('Session ID: %s' % self.uuid)
        if extra_data is None:
            self.extra_data = {}
        else:
            self.extra_data = deepcopy(extra_data)
        self.taskq = PriorityQueue()
        self.taskq_size_limit = max(100, network_threads * 2)
        self.resultq = Queue()
        self.shutdown_event = Event()
        self.fatal_error_happened = Event()
        self.retry_limit = retry_limit
        self.stat = Stat(
            speed_keys='crawler:request-processed',
            logging_enabled=stat_logging,
            logging_format=stat_logging_format,
        )
        self.fatalq = Queue()
        self.network = self.network_service_class(
            self.taskq, self.resultq,
            fatalq=self.fatalq,
            threads=network_threads,
            shutdown_event=self.shutdown_event,
            setup_request_hook=self.setup_request_hook,
            setup_request_proxy_hook=self.setup_request_proxy_hook,
            prepare_response_hook=self.prepare_response_hook,
            stat=self.stat,
        )
        self.result_workers = result_workers
        self._run_started = None

        self.dataopq = {}
        self.dataop_lock = defaultdict(Lock)
        self.dataop_counters = defaultdict(lambda: {
            'number': 0,
            'size': 0,
        })
        self.error_logger = ErrorLogger()
        self.stop_on_handler_error = stop_on_handler_error
        self.proxylist = None
        self.debug = debug
        self.num_task_generators = num_task_generators
        self.master_taskq_cfg = master_taskq

        self.init_hook()

    @classmethod
    def update_arg_parser(cls, parser):
        for key, config in cls.extra_cli_args().items():
            parser.add_argument('--extra-%s' % key, **config)

    @classmethod
    def extra_cli_args(cls):
        return {}

    def load_proxylist(self, list_type, list_location, **kwargs):
        self.proxylist = ProxyList.create_from_source(
            list_type, list_location, **kwargs
        )

    def is_dataopq_dump_time(self, name):
        to_dump = False
        try:
            number_th = self.dataop_threshold[name]['number']
        except KeyError:
            number_th = self.dataop_threshold_default['number']
        if number_th:
            if self.dataop_counters[name]['number'] >= number_th:
                    to_dump = True
        if not to_dump:
            try:
                size_th = self.dataop_threshold[name]['size']
            except KeyError:
                size_th = self.dataop_threshold_default['size']
            if size_th:
                if self.dataop_counters[name]['size'] >= size_th:
                    to_dump = True
        return to_dump

    def enq_dataop(self, name, op, size=None, force_dump=False):
        if op:
            self.enq_dataop_hook(name, op)
        self.dataop_lock[name].acquire()
        released = False
        try:
            self.dataopq.setdefault(name, [])
            if op:
                self.dataopq[name].append(op)
                self.dataop_counters[name]['number'] += 1
                if size:
                    self.dataop_counters[name]['size'] += size

            if force_dump or self.is_dataopq_dump_time(name):
                #logging.debug('Dumping data ops')
                self.stat.inc('dataop-dump-%s' % name)
                ops = self.dataopq[name]
                if ops:
                    self.dataopq[name] = []
                    self.dataop_counters[name]['number'] = 0
                    self.dataop_counters[name]['size'] = 0
                    # release as soon as possible
                    self.dataop_lock[name].release()
                    released = True
                    func = getattr(self, 'dataop_handler_%s' % name)
                    func(ops)
                else:
                    self.dataop_lock[name].release()
                    released = True
        finally:
            if not released:
                self.dataop_lock[name].release()

    def enq_dataop_hook(self, name, op):
        pass

    def init_hook(self):
        pass

    def prepare_response_hook(self, transport, req, res, urllib3_response):
        pass

    def setup_request_proxy_hook(self, transport, req):
        if self.proxylist:
            proxy = self.proxylist.random_server()
            req.setup(
                proxy=proxy.address(),
                proxy_auth=proxy.auth(),
                proxy_type=proxy.proxy_type,
            )
            # If requst is configured to not close connection (default)
            # and proxylist requires to close connection
            # then update request config
            if (
                    not req['close_connection']
                    and self.proxylist.close_connection
                ):
                req.setup(close_connection=True)

    def setup_request_hook(self, transport, req):
        pass

    def submit_task(self, req):
        self.submit_task_hook(req)
        self.taskq.put((req.priority, req))

    def submit_task_hook(self, req):
        pass

    def task_generator_master(self):
        cfg = self.master_taskq_cfg
        if not cfg:
            raise IowebConfigError('Master task queue is not configured')
        backend_id = cfg.pop('backend', None)
        if backend_id not in ('redis',):
            raise IowebConfigError(
                'Invalid master task queue backend: %s' % backend_id
            )
        # Redis specific things
        # TODO: move into backend class
        taskq_id = cfg.pop('taskq_id', None)
        if not taskq_id:
            raise IowebConfigError(
                'Invalid queue ID: %s' % taskq_id
            )
        from redis import Redis
        rdb = Redis(decode_responses=True, **cfg)
        DONE = False
        none_task_time = time.time()
        while True:
            task = rdb.lpop(taskq_id)
            if task is None:
                if time.time() - none_task_time > 5:
                    none_task_time = time.time()
                    self._flush_dataops()
                time.sleep(0.01)
            else:
                task = json.loads(task)
                if '$op' in task:
                    if task['$op'] == 'shutdown':
                        return
                    else:
                        raise IowebConfigError(
                            'Got invalid $op from master taskq queue: %s'
                            % task['$op']
                        )
                else:
                    req = Request.from_data(task)
                    yield req

    def thread_task_generator(self):
        try:
            try:
                if self.master_taskq_cfg:
                    tgen_iter = self.task_generator_master()
                else:
                    tgen_iter = iter(self.task_generator())
            except TypeError:
                return
            else:
                for item in tgen_iter:
                    while item:
                        if self.shutdown_event.is_set():
                            return
                        if self.taskq.qsize() >= self.taskq_size_limit:
                            time.sleep(self._taskgen_sleep_time)
                        else:
                            self.submit_task(item)
                            item = None
        except (Exception, KeyboardInterrupt) as ex:
            self.fatalq.put((sys.exc_info(), None))

    def is_result_ok(self, req, res):
        if res.error:
            return False
        elif isinstance(req, CallbackRequest):
            return True
        elif (
                0 < res.status < 400
                or res.status == 404
                or (
                    req.config['extra_valid_status']
                    and res.status in req.config['extra_valid_status']
                )
            ):
            return True
        else:
            return False

    def thread_result_processor(self, pause):
        error_ctx = None
        try:
            while not self.shutdown_event.is_set():
                if pause.pause_event.is_set():
                    pause.process_pause()
                try:
                    result = self.resultq.get(True, 0.1)
                except Empty:
                    pass
                else:
                    self.stat.inc('crawler:request-processed')
                    try:
                        if (
                                result['request']['raw']
                                or self.is_result_ok(
                                    result['request'],
                                    result['response'],
                                )
                            ):
                            self.process_ok_result(result)
                        else:
                            self.process_fail_result(result)
                    except Exception as ex:
                        error_ctx = collect_error_context(result['request'])
                        raise
        except (KeyboardInterrupt, Exception) as ex:
            self.fatalq.put((sys.exc_info(), error_ctx))

    def thread_fatalq_processor(self):
        try:
            while not self.shutdown_event.is_set():
                try:
                    exc_info, ctx = self.fatalq.get(True, 0.1)
                except Empty:
                    pass
                else:
                    self.shutdown_event.set()
                    self.fatal_error_happened.set()
                    logging.error('Fatal exception')
                    if ctx:
                        logging.error('Exception context:')
                        for key, val in sorted(ctx.items(), key=lambda x: x[0]):
                            logging.error(' * %s: %s' % (key, val))
                    else:
                        logging.error('Exception context: N/A')
                    logging.error(''.join(format_exception(*exc_info)))
                    if not isinstance(exc_info[1], KeyboardInterrupt):
                        self.log_error(exc_info, ctx)
        except Exception as ex:
            self.shutdown_event.set()
            raise

    def log_error(self, exc_info, ctx=None):
        ctx = ctx or {}
        ctx.update({
            'crawler_id': self.__class__.__name__,
            'date': datetime.utcnow().isoformat(),
        })
        self.error_logger.log_error(exc_info, ctx)

    def thread_manager(self, task_gens, pauses):
        try:
            [x.join() for x in task_gens]

            def system_is_busy():
                return (
                    self.taskq.qsize()
                    or self.resultq.qsize()
                    or len(self.network.active_handlers)
                )

            while not self.shutdown_event.is_set():
                while system_is_busy():
                    if self.shutdown_event.is_set():
                        return
                    time.sleep(0.1)

                for pause in pauses:
                    pause.pause_event.set()
                ok = True
                for pause in pauses:
                    if not pause.is_paused.wait(0.1):
                        ok = False
                        break
                if not ok:
                    for pause in pauses:
                        pause.pause_event.clear()
                        pause.resume_event.set()
                else:
                    if not system_is_busy():
                        for pause in pauses:
                            pause.pause_event.clear()
                            pause.resume_event.set()
                        self.shutdown_event.set()
                        return
                    else:
                        for pause in pauses:
                            pause.pause_event.clear()
                            pause.resume_event.set()
        except (KeyboardInterrupt, Exception) as ex:
            self.fatalq.put((sys.exc_info(), None))

    def process_ok_result(self, result):
        self.stat.inc('crawler:request-ok')
        name = result['request'].config['name']
        handler = getattr(self, 'handler_%s' % name)
        try:
            handler_result = handler(
                result['request'],
                result['response'],
            )
            try:
                iter(handler_result)
            except TypeError:
                pass
            else:
                for item in handler_result:
                    if isinstance(item, BaseRequest):
                        self.submit_task(item)
                    else:
                        raise Exception(
                            'Handler yielded non request task: %s' % item
                        )
        except Exception as ex:
            self.stat.inc('result-handler-error:%s' % get_error_tag(ex))
            if isinstance(ex, DataNotValid):
                self.process_fail_result(result)
            else:
                if self.stop_on_handler_error:
                    raise
                else:
                    logging.exception('Error in result handler')
                    ctx = collect_error_context(result['request'])
                    self.log_error(sys.exc_info(), ctx)

    def process_fail_result(self, result):
        self.stat.inc('crawler:request-fail')
        req = result['request']

        if result['response'].error:
            self.stat.inc('network-error:%s' % get_error_tag(
                result['response'].error
            ))
        if result['response'].status:
            self.stat.inc('http:status-%s' % result['response'].status)

        if req.retry_count + 1 < self.retry_limit:
            self.stat.inc('crawler:request-retry')
            req.retry_count += 1
            req.priority = req.priority - 1
            self.submit_task(req)
        else:
            self.stat.inc('crawler:request-rejected')
            name = result['request'].config['name']
            handler = getattr(self, 'rejected_handler_%s' % name, None)
            if handler is None:
                handler = self.default_rejected_handler
            try:
                handler(result['request'], result['response'])
            except Exception as ex:
                self.stat.inc('rejected-handler-error:%s' % get_error_tag(ex))
                if self.stop_on_handler_error:
                    raise
                else:
                    logging.exception('Error in rejected result handler')
                    ctx = collect_error_context(req)
                    self.log_error(sys.exc_info(), ctx)

    def default_rejected_handler(self, req, res):
        pass

    def run_hook(self):
        pass

    def thread_debug(self):
        try:
            while not self.shutdown_event.is_set():
                stat = []
                now = time.time()
                for hdl in self.network.active_handlers:
                    stat.append((hdl, self.network.registry[hdl]['start']))
                with open('var/crawler.debug', 'w') as out:
                    for hdl, start in list(sorted(stat, key=lambda x: (x[1] or now), reverse=True)):
                        req = self.network.registry[hdl]['request']
                        out.write('%.2f - [#%s] - %s\n' % (
                            (now - start) if start else 0,
                            req.retry_count if req else 'NA',
                            urlsplit(req['url']).netloc if req else 'NA',
                        ))
                    out.write('Active handlers: %d\n' % len(self.network.active_handlers))
                    out.write('Idle handlers: %d\n' % len(self.network.idle_handlers))
                    out.write('Taskq size: %d\n' % self.taskq.qsize())
                    out.write('Resultq size: %d\n' % self.resultq.qsize())

                total = 0
                count = 0
                for hdl, start in stat:
                    if start:
                        total += (now - start)
                        count += 1
                logging.debug('Median handler time: %.2f' % ((total / count) if count else 0))

                self.shutdown_event.wait(3)
        except (KeyboardInterrupt, Exception) as ex:
            self.fatalq.put((sys.exc_info(), None))


    def thread_network(self):
        try:
            self.network.run()
        except (KeyboardInterrupt, Exception) as ex:
            self.fatalq.put((sys.exc_info(), None))

    def _flush_dataops(self):
        for name in list(self.dataopq.keys()):
            self.enq_dataop(name, None, force_dump=True)

    def shutdown(self):
        self._flush_dataops()
        self.shutdown_hook()
        if self.stat.th_export:
            self.stat.th_export_dump_stat()

    def shutdown_hook(self):
        pass

    def run(self):
        try:
            self.run_hook()
            self._run_started = time.time()

            th_fatalq_proc = Thread(target=self.thread_fatalq_processor)
            th_fatalq_proc.start()

            task_gens = []
            if (
                    self.master_taskq_cfg
                    and self.num_task_generators > 1
                ):
                raise IowebConfigError(
                    'num_task_generators must be 1 in'
                    ' master task queue mode'
                )
            for _ in range(self.num_task_generators):
                th = Thread(target=self.thread_task_generator)
                th.start()
                task_gens.append(th)

            th_debug = Thread(target=self.thread_debug)
            if self.debug:
                th_debug.start()

            pauses = [x['pause'] for x in self.network.registry.values()]
            result_workers = []
            for _ in range(self.result_workers):
                pause = Pause()
                th = Thread(
                    target=self.thread_result_processor,
                    args=[pause],
                ) 
                pauses.append(pause)
                th.start()
                result_workers.append(th)

            th_manager = Thread(
                target=self.thread_manager,
                args=[task_gens, pauses],
            )
            th_manager.start()

            th_network = Thread(
                target=self.thread_network,
            )
            th_network.start()

            th_manager.join()
            th_fatalq_proc.join()
            [x.join() for x in task_gens]
            if self.debug:
                th_debug.join()
            [x.join() for x in result_workers]

        except (Exception, KeyboardInterrupt):
            self.fatal_error_happened.set()
            raise
        finally:
            self.shutdown_event.set()
            self.shutdown()

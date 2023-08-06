from queue import Empty
import time
import sys
import logging
from collections import deque
from threading import Thread, Event
from uuid import uuid4
import traceback
from contextlib import contextmanager

from urllib3 import PoolManager
# This is only part of ioweb where I use gevent
# explicitly. My idea is be able to run ioweb
# on native thread also.
# If ioweb is started in threaded mode then
# just use Dummy Timeout class
try:
    from gevent import Timeout
except ImportError:
    @contextmanager
    def Timeout(*args, **kwargs):
        yield


from .transport import Urllib3Transport
from .util import debug, Pause
from .response import Response
from .error import (
    DataNotValid, NetworkError, OperationTimeoutError, collect_error_context
)
from .request import Request, CallbackRequest

network_logger = logging.getLogger(__name__)


def log_network_request(req):
    if isinstance(req, Request):
        if req.retry_count > 0:
            retry_str = ' [retry=#%d]' % req.retry_count
        else:
            retry_str = ''
        if req['proxy']:
            proxy_str = ' [proxy=%s, type=%s, auth=%s]' % (
                req['proxy'],
                req['proxy_type'].upper(),
                ('YES' if req['proxy_auth'] else 'NO'),
            )
        else:
            proxy_str = ''
        network_logger.debug(
            '%s %s%s%s', req.method(), req['url'], retry_str, proxy_str
        )


class NetworkService(object):
    transport_class = Urllib3Transport

    def __init__(
            self,
            taskq,
            resultq,
            fatalq,
            resultq_size_limit=None,
            threads=3,
            shutdown_event=None,
            setup_request_hook=None,
            prepare_response_hook=None,
            setup_request_proxy_hook=None,
            stat=None,
        ):
        # Input arguments
        self.taskq = taskq
        self.resultq = resultq
        self.fatalq = fatalq
        self.num_threads = threads
        if resultq_size_limit is None:
            resultq_size_limit = self.num_threads * 2
        self.resultq_size_limit = resultq_size_limit
        self.shutdown_event = shutdown_event
        self.setup_request_hook = setup_request_hook
        self.prepare_response_hook = prepare_response_hook
        self.setup_request_proxy_hook = setup_request_proxy_hook
        self.setup_request_proxy_hook = setup_request_proxy_hook
        self.stat = stat
        # Init logic
        self.idle_handlers = set()
        self.active_handlers = set()
        self.registry = {}
        self.threads = {}

    def run(self):
        for _ in range(self.num_threads):
            ref = object()
            self.idle_handlers.add(ref)
            pause = Pause()
            transport = self.transport_class(
                prepare_response_hook=self.prepare_response_hook
            )
            self.registry[ref] = {
                'transport': transport,
                'request': None,
                'response': None,
                'start': None,
                'pause': pause,
            }
            th = Thread(
                target=self.thread_network,
                args=[ref, pause, transport],
            )
            th.daemon = True
            th.start()
            self.threads[ref] = th

    def thread_network(self, ref, pause, transport):
        req = None
        try:
            while not self.shutdown_event.is_set():
                if pause.pause_event.is_set():
                    pause.process_pause()
                    print('pause processed')

                req = None
                if self.resultq.qsize() < self.resultq_size_limit:
                    try:
                        prio, req = self.taskq.get(True, 0.1)
                    except Empty:
                        pass
                    if req:
                        self.idle_handlers.remove(ref)
                        self.active_handlers.add(ref)
                        try:
                            res = Response()
                            transport.prepare_request(req, res)
                            if self.setup_request_hook:
                                self.setup_request_hook(transport, req)
                            if self.setup_request_proxy_hook:
                                self.setup_request_proxy_hook(transport, req)
                                self.process_request(ref, transport, req, res)
                        finally:
                            req = None
                            self.free_handler(ref)
                else:
                    time.sleep(0.01)
        except Exception as ex:
            ctx = collect_error_context(req)
            self.fatalq.put((sys.exc_info(), ctx))


    def process_request(self, ref, transport, req, res):
        self.registry[ref]['request'] = req
        self.registry[ref]['response'] = res
        self.registry[ref]['start'] = time.time()
        log_network_request(req)
        try:
            timeout_time = req['timeout'] or 31536000
            with Timeout(
                    timeout_time,
                    OperationTimeoutError(
                        'Timed out while reading response',
                        Timeout(timeout_time),
                    )
                ):
                if isinstance(req, CallbackRequest):
                    req['network_callback'](req, res)
                else:
                    transport.request(req, res)
        except OperationTimeoutError as ex:
            #logging.error(ex)
            error = ex
        except (req.retry_errors or (NetworkError, DataNotValid)) as ex:
            #logging.error(ex)
            error = ex
        except Exception as ex:
            #logging.error(ex)
            raise
        else:
            error = None
        if isinstance(req, CallbackRequest):
            res.error = error
        else:
            transport.prepare_response(
                req, res, error, raise_network_error=False
            )
        self.resultq.put({
            'request': req,
            'response': res,
        })

    def free_handler(self, ref):
        self.active_handlers.remove(ref)
        self.idle_handlers.add(ref)
        self.registry[ref]['request'] = None
        self.registry[ref]['response'] = None
        self.registry[ref]['start'] = None

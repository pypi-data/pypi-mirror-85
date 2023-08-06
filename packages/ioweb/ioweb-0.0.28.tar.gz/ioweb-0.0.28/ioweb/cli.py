from pprint import pprint
import sys
import re
import time
import os.path
#import json
from bson import json_util as json
import logging
from argparse import ArgumentParser
from importlib import import_module
from collections import defaultdict
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
import code, traceback, signal
from random import SystemRandom
from hashlib import md5
from glob import glob

import psutil
from ioweb.stat import Stat

from pythonjsonlogger import jsonlogger

from .crawler import Crawler

logger = logging.getLogger('crawler.cli')

#from pympler import tracker
#mem_tracker = tracker.SummaryTracker()

def debug_handler(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""

    pass
    #import gc
    #from pympler import asizeof

    #objs = gc.get_objects()
    #mem = asizeof.asizeof(objs)
    #print('all objects memory: %s' % mem)

    #d={'_frame':frame, 'mem_tracker': mem_tracker}         # Allow access to frame object.
    #d.update(frame.f_globals)  # Unless shadowed by global
    #d.update(frame.f_locals)

    #i = code.InteractiveConsole(d)
    #message  = "Signal received : entering python shell.\nTraceback:\n"
    #message += ''.join(traceback.format_stack(frame))
    #i.interact(message)


def find_crawlers_in_module(mod, reg):
    for key in dir(mod):
        val = getattr(mod, key)
        if (
                isinstance(val, type)
                and issubclass(val, Crawler)
                and val is not Crawler
            ):
            logger.error(
                'Found crawler %s in module %s',
                val.__name__, mod.__file__
            )
            reg[val.__name__] = val


def collect_crawlers():
    reg = {}

    # Give crawlers in current directory max priority
    # Otherwise `/web/crawler/crawlers` packages are imported
    # when crawler is installed with `pip -e /web/crawler`
    sys.path.insert(0, os.getcwd())

    for location in ('crawlers',):
        try:
            mod = import_module(location)
        except ImportError as ex:
            #if path not in str(ex):
            logger.exception('Failed to import %s', location)
        else:
            if getattr(mod, '__file__', '').endswith('__init__.py'):
                dir_ = os.path.split(mod.__file__)[0]
                for fname in os.listdir(dir_):
                    if (
                        fname.endswith('.py')
                        and not fname.endswith('__init__.py')
                    ):
                        target_mod = '%s.%s' % (location, fname[:-3])
                        try:
                            mod = import_module(target_mod)
                        except ImportError as ex:
                            #if path not in str(ex):
                            logger.exception('Failed to import %s', target_mod)
                        else:
                            find_crawlers_in_module(mod, reg)
            else:
                find_crawlers_in_module(mod, reg)

    return reg


def setup_logging(logging_format='text', network_logs=False, verbose=False):#, control_logs=False):
    assert logging_format in ('text', 'json')

    root_logger = logging.getLogger()
    while root_logger.handlers:
        root_logger.handlers.pop()
    #logging.basicConfig(level=logging.DEBUG)
    if not verbose:
        logging.getLogger('urllib3.connectionpool').setLevel(level=logging.ERROR)
        logging.getLogger('urllib3.util.retry').setLevel(level=logging.ERROR)
        logging.getLogger('urllib3.poolmanager').setLevel(level=logging.ERROR)
        logging.getLogger('ioweb.urllib3_custom').setLevel(level=logging.ERROR)
        logging.getLogger('socks').setLevel(level=logging.INFO)
        if not network_logs:
            logging.getLogger('ioweb.network_service').propagate = False
    #if not control_logs:
    #    logging.getLogger('crawler.control').propagate = False

    hdl = logging.StreamHandler()
    logger = logging.getLogger()
    logger.addHandler(hdl)
    logger.setLevel(logging.DEBUG)
    if logging_format == 'json':
        #for hdl in logging.getLogger().handlers:
        hdl.setFormatter(jsonlogger.JsonFormatter())


def format_elapsed_time(total_sec):
    hours = minutes = 0
    if total_sec > 3600:
        hours, total_sec = divmod(total_sec, 3600)
    if total_sec > 60:
        minutes, total_sec = divmod(total_sec, 60)
    return '%02d:%02d:%.2f' % (hours, minutes, total_sec)


def get_crawler(crawler_id):
    reg = collect_crawlers()
    if crawler_id not in reg:
        sys.stderr.write(
            'Could not find %s crawler\n' % crawler_id
        )
        sys.exit(1)
    else:
        return reg[crawler_id]


def run_subcommand_crawl(opts):
    #logging.basicConfig(level=logging.DEBUG)
    setup_logging(
        logging_format=opts.logging_format,
        network_logs=opts.network_logs,
        verbose=opts.verbose
    )#, control_logs=opts.control_logs)
    cls = get_crawler(opts.crawler_id)
    extra_data = {}
    for key in cls.extra_cli_args():
        opt_key = 'extra_%s' % key.replace('-', '_')
        extra_data[key] = getattr(opts, opt_key)
    bot = cls(
        network_threads=opts.network_threads,
        extra_data=extra_data,
        debug=opts.debug,
        stat_logging=(opts.stat_logging == 'yes'),
        stat_logging_format=opts.stat_logging_format,
        master_taskq=(
            json.loads(opts.master_taskq)
            if opts.master_taskq else None
        ),
    )
    try:
        bot.run()
    except KeyboardInterrupt:
        logging.debug('Got INT signal')
        bot.fatal_error_happened.set()
    logging.debug('Stats:')
    for key, val in sorted(bot.stat.total_counters.items()):
        logging.debug(' * %s: %s' % (key, val))
    if bot._run_started:
        logging.debug('Elapsed: %s' % format_elapsed_time(time.time() - bot._run_started))
    else:
        logging.debug('Elapsed: NA')
    if bot.fatal_error_happened.is_set():
        sys.exit(1)
    else:
        sys.exit(0)


def get_master_taskq_id(crawler_id):
    # uniq key is hex unix seconds + random 4 hex chars
    uniq_key = '%s_%s' % (
        '%x' % int(time.time()),
        '%04x' % int(SystemRandom().randint(0, 9999)),
    )
    return 'ioweb_taskq_%s_%s' % (
        crawler_id.lower(),
        uniq_key
    )


def thread_worker(
        crawler_id, threads, stat, preg,
        evt_error, evt_init,
        master_taskq=False, master_taskq_id=None
    ):
    counters = defaultdict(int)
    try:
        if master_taskq:
            master_taskq_cfg = json.dumps({
                'backend': 'redis',
                'taskq_id': master_taskq_id,
                'db': 13,
            })
        else:
            master_taskq_cfg = ''

        cmd = [
            'ioweb',
            'crawl',
            crawler_id,
            '-t%d' % threads,
            '--logging-format=json',
            '--stat-logging-format=json',
            '--master-taskq=%s' % master_taskq_cfg,
        ]
        proc = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        preg[proc.pid] = proc
    finally:
        evt_init.set()
    while True:
        line = proc.stdout.readline()
        try:
            obj = json.loads(line.decode('ascii'))
        except (ValueError, UnicodeDecodeError):
            uline = line.decode('utf-8', errors='replace')
            logging.error(
                '[pid=%d] RAW-MSG: %s',
                proc.pid, uline.rstrip()
            )
        else:
            msg = obj['message']
            if 'exc_info' in obj:
                msg += obj['exc_info']
            try:
                msg_obj = json.loads(msg)
            except ValueError:
                logging.error('[pid=%d] TEXT-MSG: %s', proc.pid, msg)
            else:
                if 'eps' in msg_obj and 'counter' in msg_obj:
                    for key in msg_obj['eps'].keys():
                        stat.speed_keys = set(stat.speed_keys) | set([key])
                    for key, val in msg_obj['counter'].items():
                        delta = val - counters[key]
                        counters[key] = val
                        stat.inc(key, delta)
                else:
                    logging.error('[pid=%d] JSON-MSG: %s', proc.pid, msg_obj)
        ret = proc.poll()
        if ret is not None:
            if ret !=0:
                evt_error.set()
            break


def thread_task_gen(crawler_id, workers, evt_error, taskq_id):
    try:
        from redis import Redis
        rdb = Redis(db=13)
        cls = get_crawler(crawler_id)
        bot = cls(stat_logging=False)
        try:
            tgen_iter = iter(bot.task_generator())
        except TypeError:
            return
        else:
            try:
                taskq_cap = workers * bot.taskq_size_limit
                for task in tgen_iter:
                    while True:
                        if rdb.llen(taskq_id) < taskq_cap:
                            break
                        else:
                            time.sleep(0.01)
                    rdb.rpush(taskq_id, json.dumps(task.as_data()))
            finally:
                for _ in range(workers):
                    rdb.rpush(taskq_id, json.dumps({
                        '$op': 'shutdown',
                    }))
    except Exception:
        logging.exception('Error in thread_task_gen')
        evt_error.set()


def run_subcommand_multi(opts):
    setup_logging(
        logging_format='text',
        network_logs=True,
    )
    stat = Stat()

    pool = []
    preg = {}
    evt_error = Event()
    evt_stop = Event()
    try:
        if opts.master_taskq:
            master_taskq_id = get_master_taskq_id(opts.crawler_id)
            th_task_gen = Thread(
                target=thread_task_gen,
                args=[
                    opts.crawler_id, opts.workers, evt_error,
                    master_taskq_id
                ],
            )
            th_task_gen.daemon = True
            th_task_gen.start()
        else:
            master_taskq_id = None

        for _ in range(opts.workers):
            evt_init = Event()
            th = Thread(
                target=thread_worker,
                args=[
                    opts.crawler_id,
                    opts.threads,
                    stat, preg, evt_error, evt_init,
                ],
                kwargs={
                    'master_taskq': opts.master_taskq,
                    'master_taskq_id': master_taskq_id,
                },
            )
            th.daemon = True
            th.start()
            pool.append(th)
            evt_init.wait()

        mem_check_time = time.time()

        while (
                not evt_stop.is_set()
                and not evt_error.is_set()
            ):
            num_done = 0
            for proc in preg.values():
                try:
                    proc.wait(timeout=0.1)
                except TimeoutExpired:
                    pass
                else:
                    num_done += 1
                if evt_error.is_set():
                    break
                if num_done == len(pool):
                    evt_stop.set()
                    break

                if opts.rss_limit:
                    if time.time() - mem_check_time > 5:
                        for proc in preg.values():
                            ps_proc = psutil.Process(proc.pid)
                            rss_mb = (
                                ps_proc.memory_info().rss
                                / (1024.0 * 1024)
                            )
                            if rss_mb > opts.rss_limit:
                                logging.error(
                                    'Terminating process, pid=%d, rss=%.02f mb, limit=%d mb' % (
                                        proc.pid, rss_mb, opts.rss_limit
                                    )
                                )
                                proc.terminate()
    finally:
        for proc in preg.values():
            logging.debug('[!] Finishing crawler subprocess, pid=%d' % proc.pid)
            proc.terminate()
            proc.wait()


def command_ioweb():
    #signal.signal(signal.SIGUSR1, debug_handler)

    parser = ArgumentParser()#add_help=False)

    crawler_cls = None
    if len(sys.argv) > 2:
        if sys.argv[1] == 'crawl':
            crawler_cls = get_crawler(sys.argv[2])

    subparsers = parser.add_subparsers(
        dest='command',
        title='Subcommands of ioweb command',
        description='',
    )

    # Crawl
    crawl_subparser = subparsers.add_parser(
        'crawl', help='Run crawler',
    )
    crawl_subparser.add_argument('crawler_id')
    crawl_subparser.add_argument('-t', '--network-threads', type=int, default=1)
    crawl_subparser.add_argument('-n', '--network-logs', action='store_true', default=False)
    crawl_subparser.add_argument('--debug', action='store_true', default=False)
    crawl_subparser.add_argument('-v', '--verbose', action='store_true', default=False)
    crawl_subparser.add_argument(
        '--stat-logging', choices=['yes', 'no'], default='yes',
    )
    crawl_subparser.add_argument(
        '--stat-logging-format', choices=['text', 'json'], default='text',
    )
    crawl_subparser.add_argument(
        '--logging-format', choices=['text', 'json'], default='text',
    )
    #parser.add_argument('--control-logs', action='store_true', default=False)
    crawl_subparser.add_argument(
        '--master-taskq', type=str
    )
    crawl_subparser.add_argument(
        '--profile', action='store_true', default=False
    )
    crawl_subparser.add_argument(
        '--profile-clock-type', choices=['cpu', 'wall'], default='cpu'
    )
    if crawler_cls:
        crawler_cls.update_arg_parser(crawl_subparser)

    # multi
    multi_subparser = subparsers.add_parser(
        'multi', help='Run multi instances of crawler',
    )
    multi_subparser.add_argument('crawler_id')
    multi_subparser.add_argument(
        '-w', '--workers', type=int, default=1,
        help='Number of crawler processes to spawn',
    )
    multi_subparser.add_argument(
        '-t', '--threads', type=int, default=1,
        help='Number of thread in each crawler process',
    )
    multi_subparser.add_argument(
        '--master-taskq', action='store_true', default=False,
        help='Serve tasks from parent process',
    )
    multi_subparser.add_argument('--rss-limit', type=int)

    opts = parser.parse_args()
    if opts.command == 'crawl':
        if opts.profile:
            import yappi
            yappi.set_clock_type(opts.profile_clock_type)
            yappi.start()
        try:
            run_subcommand_crawl(opts)
        finally:
            if opts.profile:
                yappi.stop()
                threads = yappi.get_thread_stats()
                for fname in glob('var/prof/*.prof'):
                    os.unlink(fname)
                for th in threads:
                    stats = yappi.get_func_stats(ctx_id=th.id)
                    stats.save('var/prof/%s.prof' % th.id, type='callgrind')
                stats = yappi.get_func_stats()
                stats.save('var/prof/all.prof', type='callgrind')

    elif opts.command == 'multi':
        run_subcommand_multi(opts)
    else:
        parser.print_help()

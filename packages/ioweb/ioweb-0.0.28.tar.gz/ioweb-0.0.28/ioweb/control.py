import json
from pprint import pprint, pformat
import logging
from threading import Thread
import time
import socket

from ioweb import request
from ioweb.error import NetworkError


class ControlThread(object):
    def __init__(self, bot, ping_url, token, tags=None):
        self.bot = bot
        self.ping_url = ping_url
        self.token = token
        self.tags = (tags or {})

    def start(self):
        th = Thread(target=self.thread_worker)
        th.daemon = True
        th.start()

    def thread_worker(self):
        op_time = 0
        op_period = 10
        while True:
            now = time.time()
            if now - op_time > op_period:
                try:
                    res = request( # pytype: disable=not-callable
                        self.ping_url,
                        headers={'access-token': self.token},
                        data=json.dumps(self.build_ping_data()),
                        timeout=5
                    )
                except NetworkError as ex:
                    logging.exception('Network error in control thread')
                else:
                    if res.status != 200 or res.text != 'OK':
                        logging.error(
                            'Control server return unexpected response on ping request:'
                            ' code=%s, data=%s'
                            % (res.status, res.text[:50])
                        )
                finally:
                    op_time = now

    def build_ping_data(self):
        # init
        net = self.bot.network
        ret = {
            'handlers': [],
            'num_active_handlers': len(net.active_handlers),
            'num_idle_handlers': len(net.idle_handlers),
            'taskq_size': self.bot.taskq.qsize(),
            'resultq_size': self.bot.resultq.qsize(),
            'tags': self.tags,
            'hostname': socket.gethostname(),
            'crawler_id': self.bot.__class__.__name__,
            'session_id': self.bot.uuid,
            'stat': dict(self.bot.stat.total_counters),
        }

        total_active_time = 0
        for hdl in net.active_handlers:
            now = time.time()
            req = net.registry[hdl]['request']
            start_time = net.registry[hdl]['start']
            item = {
                'start_time': start_time,
                'active_time': (now - start_time) if start_time else 0,
                'retry_count': req.retry_count if req else None,
                'url': req['url'] if req else None,
                # todo: all req data
            }
            ret['handlers'].append(item)
            total_active_time += item['active_time']

        ret['median_handler_active_time'] = (
            (total_active_time / len(ret['handlers']))
            if len(ret['handlers']) else 0
        )
        return ret

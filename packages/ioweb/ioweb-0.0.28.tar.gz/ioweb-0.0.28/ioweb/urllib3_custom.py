"""
Credit: https://github.com/Roadmaster/forcediphttpsadapter/blob/master/forcediphttpsadapter/adapters.py
"""
import logging

from urllib3.util import connection
from urllib3.connectionpool import HTTPSConnectionPool, HTTPConnectionPool
from urllib3.connection import HTTPSConnection, DummyConnection, HTTPConnection
from urllib3 import PoolManager
from urllib3.poolmanager import SSL_KEYWORDS
from socket import error as SocketError, timeout as SocketTimeout
from urllib3.exceptions import (
    ConnectTimeoutError,
    NewConnectionError,
)
from cachetools import TTLCache

log = logging.getLogger(__name__)

# urllib3 do not pass SSL server name if
# it detectes the server name is IP address
# This hack disables the IP check and makes urllib3
# thinks that any server name is not IPv4 address
import urllib3.util.ssl_
urllib3.util.ssl_.is_ipaddress = lambda x: False


class CustomHttpConnection(HTTPConnection, object):
    def __init__(self, *args, **kwargs):
        self._custom_ip = kwargs.pop('custom_ip', None)
        self._dns_host_original = None
        super(CustomHttpConnection, self).__init__(*args, **kwargs)

    @property
    def host(self):
        return self._dns_host_original

    @host.setter
    def host(self, val):
        self._dns_host_original = val
        self._dns_host = val

    @property
    def _dns_host(self):
        return self._custom_ip if self._custom_ip else self._dns_host_value

    @_dns_host.setter
    def _dns_host(self, value):
        self._dns_host_value = value


class CustomHttpsConnection(HTTPSConnection, object):
    def __init__(self, *args, **kwargs):
        self._custom_ip = kwargs.pop('custom_ip', None)
        self._dns_host_original = None
        super(CustomHttpsConnection, self).__init__(*args, **kwargs)

    @property
    def host(self):
        return self._dns_host_original

    @host.setter
    def host(self, val):
        self._dns_host_original = val
        self._dns_host = val

    @property
    def _dns_host(self):
        return self._custom_ip if self._custom_ip else self._dns_host_value

    @_dns_host.setter
    def _dns_host(self, value):
        self._dns_host_value = value


class CustomHttpConnectionPool(HTTPConnectionPool):
    ConnectionCls = CustomHttpConnection

    def __init__(self, *args, **kwargs):
        self._custom_ip = kwargs.pop('custom_ip', None)
        super(CustomHttpConnectionPool, self).__init__(*args, **kwargs)
        self.conn_kw['custom_ip'] = self._custom_ip


class CustomHttpsConnectionPool(HTTPSConnectionPool):
    ConnectionCls = CustomHttpsConnection

    def __init__(self, *args, **kwargs):
        self._custom_ip = kwargs.pop('custom_ip', None)
        super(CustomHttpsConnectionPool, self).__init__(*args, **kwargs)
        self.conn_kw['custom_ip'] = self._custom_ip

    def __str__(self):
        return ('%s(host=%r, port=%r, custom_ip=%s)' % (
            type(self).__name__,
            self.host,
            self.port,
            self._custom_ip,
        ))


class CustomPoolManager(PoolManager):
    def __init__(self, *args, **kwargs):
        super(CustomPoolManager, self).__init__(*args, **kwargs)
        self.resolving_cache = TTLCache(maxsize=10000, ttl=(60 * 60))
        self.pool_classes_by_scheme = {
            'http': CustomHttpConnectionPool,
            'https': CustomHttpsConnectionPool,
        }

    def _new_pool(self, scheme, host, port, request_context=None):
        if request_context is None:
            request_context = self.connection_pool_kw.copy()
        custom_ip = self.resolving_cache.get(host, None)
        if custom_ip:
            request_context['custom_ip'] = custom_ip
        return super(CustomPoolManager, self)._new_pool(
            scheme, host, port, request_context
        )

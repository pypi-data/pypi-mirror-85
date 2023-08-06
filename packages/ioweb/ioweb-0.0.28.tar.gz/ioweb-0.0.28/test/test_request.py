import pytest

from ioweb.request import Request


def default_config():
    req = Request()
    keys = [
        'method',
        'name',
        'url',
        'max_redirects',
        'follow_redirect',
        'timeout',
        'connect_timeout',
        'resolve',
        'raw',
        'headers',
        'content_encoding',
        'decode_content',
        'content_read_limit',
        'priority',
        'extra_valid_status',
        'proxy',
        'proxy_auth',
        'proxy_type',
        'data',
        'multipart',
        'verify',
    ]
    assert set(keys) == set(req.config.keys())

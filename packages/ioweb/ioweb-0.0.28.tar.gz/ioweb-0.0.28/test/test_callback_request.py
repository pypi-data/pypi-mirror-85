import pytest

from ioweb.request import CallbackRequest


def default_config():
    req = CallbackRequest()
    keys = [
        'name',
        'timeout',
        'raw',
        'network_callback',
    ]
    assert set(keys) == set(req.config.keys())

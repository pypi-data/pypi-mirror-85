import pytest

from ioweb.request import BaseRequest


def test_default_meta():
    req = BaseRequest()
    assert req.meta == {}


def test_custom_default_config():
    class CustomRequest(BaseRequest):
        def get_default_config(self):
            return {
                'foo': 'bar',
            }

    req = CustomRequest()
    assert req.config['foo'] == 'bar'


def test_setup_invalid_key():
    class CustomRequest(BaseRequest):
        def get_default_config(self):
            return {
                'foo': 'bar',
            }

    req = CustomRequest()
    with pytest.raises(AssertionError):
        req.setup(zzz=1)


def test_getitem_method():
    class CustomRequest(BaseRequest):
        def get_default_config(self):
            return {
                'foo': 'bar',
            }

    req = CustomRequest()
    assert req['foo'] == 'bar'


def test_getitem_method_invalid_key():
    class CustomRequest(BaseRequest):
        def get_default_config(self):
            return {
                'foo': 'bar',
            }

    req = CustomRequest()
    with pytest.raises(KeyError):
        assert req['zzz']


def test_as_data():
    class CustomRequest(BaseRequest):
        def get_default_config(self):
            return {
                'foo': 'bar',
            }

    req = CustomRequest()
    assert req.as_data()['config'] == {'foo': 'bar'}
    assert all(
        x in req.as_data()
        for x in ('config', 'meta', 'priority', 'retry_count')
    )


def test_lt():
    req1 = BaseRequest(priority=1)
    req2 = BaseRequest(priority=2)
    req3 = BaseRequest(priority=3)
    assert req2 > req1
    assert req1 < req3


def test_eq():
    req1 = BaseRequest(priority=1)
    req2 = BaseRequest(priority=2)
    req3 = BaseRequest(priority=2)
    assert req1 != req2
    assert req2 == req3


def test_from_data():
    data = {
        'config': {'foo': 'bar'},
        'meta': {'name': 'Putin'},
        'priority': 1,
        'retry_count': 0,
    }
    req = BaseRequest.from_data(data)
    assert req.config['foo'] == 'bar'
    assert req.meta['name'] == 'Putin'

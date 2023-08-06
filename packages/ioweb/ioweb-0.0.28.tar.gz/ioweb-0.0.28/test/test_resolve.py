import pytest

from ioweb.session import Session
from ioweb.error import IowebConfigError

from .fixtures import test_server, TEST_SERVER


def test_resolve(test_server):
    sess = Session()
    res = sess.request(
        url='http://ya.ru:%d/' % TEST_SERVER['port'],
        resolve={
            'ya.ru': '127.0.0.1',
        }
    )
    assert res.text == TEST_SERVER['content']


#def test_resolve_proxy(test_server):
#    sess = Session()
#    with pytest.raises(IowebConfigError):
#        res = sess.request(
#            url='http://ya.ru:%d/' % TEST_SERVER['port'],
#            resolve={
#                'ya.ru': '127.0.0.1',
#            },
#            proxy='1.1.1.1',
#        )

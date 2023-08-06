from ioweb.session import Session, request
from ioweb.crawler import Crawler, Request


def test_sess():
    sess = Session()
    res = sess.request('https://yandex.ru/robots.txt')
    assert '# yandex.ru' in res.text


def test_request():
    res = request('https://yandex.ru/robots.txt')
    assert '# yandex.ru' in res.text


def test_crawler():

    class TestCrawler(Crawler):
        def task_generator(self):
            yield Request(
                name='page',
                url='https://yandex.ru/robots.txt'
            )

            def test_page(self, req, res):
                assert '# yandex.ru' in res.text

    bot = TestCrawler()
    bot.run()

import time

from ioweb.crawler import Crawler, Request


class TestCrawler(Crawler):
    def task_generator(self):
        while True:
            yield Request(
                name='page',
                url='https://yandex.ru/robots.txt'
            )
            time.sleep(0.1)

    def handler_page(self, req, res):
        assert '# yandex.ru' in res.text

bot = TestCrawler()
bot.run()

import asyncio

from common.log import get_logger
from common.time_counter import time_limit
from core.downloader import Downloader
from core.scheduler import Scheduler


class Engine:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    # 显示方法执行的时间
    @time_limit(display=True)
    def run(self, spider_class):
        spider = spider_class.from_crawler()
        if not hasattr(spider, "custom_settings"):
            spider.custom_settings = {}

        downloader = Downloader(spider)
        scheduler = Scheduler(spider)

        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(scheduler.crawl(spider, downloader))
        try:
            loop.run_until_complete(task)
        finally:
            loop.close()

    def __del__(self):
        self.logger.info("Engine quit.")

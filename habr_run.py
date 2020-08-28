from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parse import settings
from parse.spiders.hubr import HubrSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(HubrSpider)
    crawl_proc.start()
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

#--------run avito--------
# from parse import settings
# from parse.spiders.avito import AvitoSpider
#
# if __name__ == '__main__':
#     crawl_settings = Settings()
#     crawl_settings.setmodule(settings)
#     crawl_proc = CrawlerProcess(settings=crawl_settings)
#     crawl_proc.crawl(AvitoSpider)
#     crawl_proc.start()


#--------run hubr--------
# from parse import settings
# from parse.spiders.hubr import HubrSpider
#
# if __name__ == '__main__':
#     crawl_settings = Settings()
#     crawl_settings.setmodule(settings)
#     crawl_proc = CrawlerProcess(settings=crawl_settings)
#     crawl_proc.crawl(HubrSpider)
#     crawl_proc.start()


#--------run Instagram--------
from parse import settings
from parse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(InstagramSpider,
                     'Login',
                     '#PWD_INSTAGRAM_BROWSER:',
                     ['page_user'])
    crawl_proc.start()
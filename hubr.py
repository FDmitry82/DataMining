import scrapy
from scrapy.http import Response
from pymongo import MongoClient

class HubrSpider(scrapy.Spider):
    name = 'habr'
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru/all/'
                  ]

    xpath_query = {
        'links_article': '//div[contains(@class, "posts_list")]//h2//a/@href',


    }

    data_base_client = MongoClient()

    def parse(self, response: Response):
        for link in response.xpath(self.xpath_query['links_article']):
            yield response.follow(link, callback=self.ads_item_parse)

    def ads_item_parse(self, response: Response):
        db = self.data_base_client['db_habr']
        collection = db['habr_blog']
        title = response.xpath('//span[@class="post__title-text"]/text()').extract_first()
        url_stat = response.request._get_url()
        name_autor = response.xpath('//span[contains(@class, "user-info__nickname")]//text()').extract_first()
        href_autor = response.xpath('//header[contains(@class, "post__meta")]//a//@href').extract_first()
        images = response.xpath('//img/@src').getall()


        collection.insert_one({'title': title, 'url_stat': url_stat, 'name_autor': name_autor, 'href_autor': href_autor, 'images': images})

        yield {'title': title, 'url_stat': url_stat, 'name_autor': name_autor, 'href_autor': href_autor, 'images': images}


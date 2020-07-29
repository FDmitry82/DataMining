import scrapy
from scrapy.http import Response
from pymongo import MongoClient

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://avito.ru/pervouralsk/nedvizhimost',
                  'https://www.avito.ru/pervouralsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1'
                  ]

    xpath_query = {
        'menu_links': '//li[contains(@class, "rubricator-list-item-item-tP77G")]//a/@href',
        'ads_items': '//div[contains(@class, "item__line")]//h3//a[contains(@class, "snippet-link")]',

    }

    data_base_client = MongoClient()

    def parse(self, response: Response):
        for link in response.xpath(self.xpath_query['menu_links']):
            yield response.follow(link, callback=self.ads_feed_parse)

    def ads_feed_parse(self, response: Response):
        for link in response.xpath(self.xpath_query['ads_items']):
            yield response.follow(link, callback=self.ads_item_parse)

    def ads_item_parse(self, response: Response):
        db = self.data_base_client['db_avito']
        collection = db['avito_nedvizhimost']
        title = response.xpath('//h1/span[@itemprop="name"]/text()').extract_first()
        price = response.xpath('//span[@itemprop="price"]/@content').extract_first()
        address = response.xpath('//span[@class="item-address__string"]/text()').extract_first()

        collection.insert_one({'titele': title, 'price': price, 'address': address})

        yield {'titele': title, 'price': price, 'address': address}


import scrapy
from copy import deepcopy
from urllib.parse import urlencode
import re
import json
from scrapy.http import Response
from pymongo import MongoClient


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    __login_url = 'https://www.instagram.com/accounts/login/ajax/'
    __api_url = '/graphql/query'
    __api_query = {
        'posts_feed': '7437567ae0de0773fd96545592359a6b',
    }

    variables = {"id": None, "first": 12}

    def __init__(self, login: str, passwd: str, parse_users: list, *args, **kwargs):
        self.parse_users = parse_users
        self.login = login
        self.passwd = passwd
        super().__init__(*args, **kwargs)

    def parse(self, response):
        token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.__login_url,
            method='POST',
            callback=self.im_login,
            formdata={
                'username': self.login,
                'enc_password': self.passwd,
            },
            headers={'X-CSRFToken': token}
        )

    def im_login(self, response):
        data = response.json()
        if data['authenticated']:
            for user_name in self.parse_users:
                yield response.follow(f'/{user_name}',
                                      callback=self.user_parse,
                                      cb_kwargs={'user_name': user_name})

    def user_parse(self, response, user_name):
        user_id = self.fetch_user_id(response.text, user_name)
        variables = deepcopy(self.variables)
        variables['id'] = f"{user_id}"
        url = f"{self.__api_url}?query_hash={self.__api_query['posts_feed']}&variables={json.dumps(variables)}"
        yield response.follow(url,
                              callback=self.user_feed_pasre,
                              cb_kwargs={'user_name': user_name,
                                         'variables': variables
                                         },
                              )

    def user_feed_pasre(self, response, user_name, variables):
        date = response.json()
        print(1)
        #todo out items for reqest
        for item in date['eges']:
            yield InstItem(item)
        print(1)
        page_info = data['data']['user']['edge_owner_to_timeline_media']['page_info']
        if page_info['has_next_page']:
            variables["after"] = page_info['end_cursor']
            url = f"{self.__api_url}?query_hash={self.__api_query['posts_feed']}&variables={json.dumps(variables)}"
            yield response.follow(url,
                                  callback=self.user_feed_pasre,
                                  cb_kwargs={'user_name': user_name,
                                             'variables': variables
                                             },
                                  )


    def fetch_user_id(self, text, username):
        """Парсит нужную строку, через регулярное выражение"""
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    def fetch_csrf_token(self,  text):
        """Используя регулярные выражения парсит переданный текст
        и возвращает csrf_token"""
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

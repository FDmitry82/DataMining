import requests
from datetime import datetime as dt
import json


special_offers_url = 'https://5ka.ru/api/v2/special_offers/'
categories_url = 'https://5ka.ru/api/v2/categories/'
params = {
    'record_per_page': 50,
    }

HEADERS = {
    'User-Agent': ('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
}

class CatalogSpecial:

    def __init__(self, categories_url, special_url, headers, params):
        self.__categories_url = categories_url
        self.__special_url = special_url
        self.__headers = headers
        self.__params = params

    def get_data_from_api(self):
        try:
            response = requests.get(self.__categories_url,
                                    headers=self.__headers,
                                    params=self.__params)
        except Exception as err:
            print(f'Fetching categories failed: {err}')
            return None
        else:
            categories = response.json()

        for special in categories:
            self.__params["categories"] =\
                f'{special["parent_group_code"]}'
            try:
                response = requests.get(
                    self.__special_url,
                    headers=self.__headers,
                    params=self.__params)
            except Exception as err:
                print(err)
            else:
                data = response.json()['results']
                if data:
                    self.save_json_to_file(special["parent_group_name"],
                                           response.json()['results'])

    def save_json_to_file(self, group_name, data):
        file_name = group_name.replace(' ', '-').replace(',', '')
        file_name = file_name + '-' + dt.now().strftime('%d-%m-%Y-%H-%M')\
            + '.json'
        try:
            with open(file_name, 'w', encoding='UTF-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False)
        except Exception as err:
            print(err)


if __name__ == "__main__":
    catalog = CatalogSpecial(categories_url, special_offers_url, HEADERS, params)
    catalog.get_data_from_api()

print ('Файлы созданы')
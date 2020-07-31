from bs4 import BeautifulSoup as bs
import requests
import json
from random import randint

main = 'https://geekbrains.ru'
url_geek = 'https://geekbrains.ru/posts'


class GeekBr:

    def __init__(self):
        self.posts_urls = set()
        self.pagination_urls = set()
        self.__done_urls = set()

    def get_page_soup(self, url):
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        return soup

    def run(self, url=None):
        url = url or url_geek
        soup = self.get_page_soup(url)
        self.pagination_urls.update(self.get_pagination(soup))
        spam = self.get_posts_urls(soup)
        self.posts_urls.update(spam)
        self.get_post_data(spam)

        for url in tuple(self.pagination_urls):
            if url not in self.__done_urls:
                self.__done_urls.add(url)
                self.run(url)

    def get_pagination(self, soup):
        ul = soup.find('ul', attrs={'class': 'gb__pagination'})
        out = [f'{main}{a.get("href")}'
               for a in ul.find_all('a') if a.get("href")]
        return out

    def get_posts_urls(self, soup):
        posts_wrap = soup.find('div', attrs={'class': 'post-items-wrapper'})
        out = [f'{main}{a.get("href")}'
               for a in posts_wrap.find_all('a', attrs={'class': 'post-item__title'})]
        return out

    def get_post_data(self, urls):
        for url in urls:
            data = {}
            eggs = self.get_page_soup(url)
            data['title'] = eggs.head.title.string
            data['post_url'] = url
            author = eggs.find(itemprop='author')
            data['writer_name'] = author.string
            data['writer_url'] = f'{main}{author.parent.attrs["href"]}'
            tags = eggs.find_all(attrs={'class': 'small'})
            data['tags_urls'] = [f'{main}{tag.get("href")}' for tag in tags
                                 if tag.get("href")]
            self.save_to_file(data)

    def save_to_file(self, data):
        file_name = str(randint(5000, 500000)) + '.json'
        if data:
            with open(file_name, 'w', encoding='UTF-8') as file_w:
                json.dump(data, file_w, ensure_ascii=False)


if __name__ == '__main__':
    parser = GeekBr()
    parser.run()

print ('Готово!')
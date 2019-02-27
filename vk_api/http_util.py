import requests
from bs4 import BeautifulSoup
from vk_api import logger


class HttpUtil:
    def __init__(self):
        self.logger = logger.Logger("Http_utils")
        self.session = requests.Session()
        self.parser = "html.parser"

    def get(self, url, params=None):
        """
        Выполнение GET запроса
        :param url:
        :param params:
        :return:
        """
        session = self.session.get(url, params=params)
        self.logger.debug({'url': url, 'params': params})
        return {'url': session.url, 'content': session.text}

    def post(self, url, params=None):
        """
        Выполнение POST запроса
        :param url:
        :param params:
        :return dict:
        """
        session = self.session.post(url, data=params)
        self.logger.debug({'url': url, 'params': params})
        return {'url': session.url, 'content': session.text}

    def parse(self, html):
        """
        Парсинг ответа, парсер html
        :param html:
        :return BeautifulSoup:
        """
        return BeautifulSoup(html, self.parser)

    def get_parse(self, url, params):
        """
        Выполение GET запроса и парсинг
        :param url:
        :param params:
        :return dict:
        """
        session = self.session.get(url, params=params)
        self.logger.debug({'url': url, 'params': params})
        return {'url': session.url, 'content': session.content, 'parse': BeautifulSoup(session.text, self.parser,)}

    def get_session(self):
        """
        Вовзращнение объекта сессии
        :return:
        """
        return self.session

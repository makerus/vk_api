import json
import time
import random

from vk_api.http_util import HttpUtil
from urllib.parse import urlparse, parse_qs

from vk_api.logger import Logger
from vk_api.tokenizer import Tokenizer


class VkApi:
    def __init__(self, options):
        """
        Создание объекта API
        :param options:
        """
        self.options = options
        self.authorize_url = "https://oauth.vk.com/authorize"
        self.redirect_uri = "http://oauth.vk.com/blank.html"
        self.action = "https://login.vk.com/?act=login&soft=1&utf8=1"
        self.method_action = "https://api.vk.com/method/"
        self.auth_config = {
                "client_id": self.options['client_id'],
                "redirect_uri": self.redirect_uri,
                "display": "mobile",
                "response_type": "token",
                "scope": self.options['scope'],
                "v": self.options['api_v'],
                "revoke": 1
            }
        self.token = None
        self.logger = Logger('vk_api')

    def login(self):
        """
        Проверка на существование уже полученного токена
        Или его повторное получение, в случае его отсутствия
        :return:
        """
        token = Tokenizer('.token', self)
        token.token_init()

    def login_api(self):
        """
        Авторизация и получение токена API VK
        """
        self.logger.log('Авторизация')
        http = HttpUtil()
        auth_page = http.get_parse(self.authorize_url, self.auth_config)
        form_el = {}
        for el in auth_page['parse'].find_all('input'):
            if 'name' in el.attrs and 'value' in el.attrs:
                form_el.update({el.attrs['name']: el.attrs['value']})
                form_el.update({'email': self.options['login'], 'pass': self.options['password']})

        response = http.parse(http.post(self.action, form_el)['content'])
        action = response.find('div', class_='form_item').form.attrs['action']
        url_token = urlparse(http.get(action)['url'])
        self.token = parse_qs(url_token.fragment, encoding='utf8')['access_token'][0]

        if self.logger is not None:
            self.logger.log('Авторизация завершена')
        else:
            self.logger.error('Ошибка авторизации')

    def query(self, name, params):
        """
        Выполнение запроса к API VK
        :param name:
        :param params:
        :return:
        """
        http = HttpUtil()
        query_param = []
        for k, v in params.items():
            query_param.append(str(str(k) + "=" + str(v)))

        url = "https://api.vk.com/method/" + name + "?" + '&'.join(query_param) +\
              "&access_token=" + self.token + "&v=" + self.options['api_v']
        query = http.get(url)
        response = json.loads(query['content'])
        time.sleep(random.randint(1, self.options['max_timeout']))
        if 'error' in response:
            return json.loads(query['content'])['error']
        else:
            return json.loads(query['content'])['response']

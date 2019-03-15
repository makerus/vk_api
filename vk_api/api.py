import json
import time
import random
import threading
import signal
import os

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
        self.commands = []
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
        self.symbol_command = '@'
        self.symbol_answer = '#'

        signal.signal(signal.SIGINT, self.handler_signal)

    def get_token(self, api):
        """
        Проверка на существование уже полученного токена
        Или его повторное получение, в случае его отсутствия
        :return:
        """
        if 'token' not in self.options:
            token = Tokenizer('.token', api)
            token.token_init()
        else:
            self.logger.log('Авторизация черезе токен группы')
            self.set_token(self.options['token'])

    def set_token(self, token):
        """
        Установка токена
        :param token:
        :return:
        """
        if token:
            self.token = token
        else:
            self.logger.error('Проверьте настройки конфигурации!')
            exit()

    def login(self):
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
        response_get_token = http.get(action)
        url_token = urlparse(response_get_token['url'])
        try:
            self.set_token(parse_qs(url_token.fragment, encoding='utf8')['access_token'][0])
        except KeyError:
            self.logger.error(json.loads(response_get_token['content']))

        if self.token is not None:
            self.logger.log('Авторизация завершена')
        else:
            self.logger.error('Ошибка авторизации')
            exit()

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

        url = "https://api.vk.com/method/" + name + "?" + '&'.join(query_param) + \
              "&access_token=" + self.token + "&v=" + self.options['api_v']
        query = http.get(url)
        response = json.loads(query['content'])
        time.sleep(self.timeout())

        if 'error' in response:
            return json.loads(query['content'])['error']
        else:
            return json.loads(query['content'])['response']

    def get_long_poll(self):
        """
        Инициализация getLongPoll
        :return:
        """
        pts = self.query('groups.getLongPollServer', {'group_id': self.options['group_id']})
        return pts

    def get_ts(self, server, key, ts):
        """
        Получение TS для API getLongPoll
        :param server:
        :param key:
        :param ts:
        :return:
        """
        http = HttpUtil()
        url_server = server + '?act=a_check&key=' + key + '&ts=' + ts + '&wait=25'
        response = http.get(url_server)
        return json.loads(response['content'])

    def init_long_poll(self):
        """
        Реализация getLongPool подключения
        :return:
        """
        pts = self.get_long_poll()
        key = pts['key']
        server = pts['server']

        while True:
            pts = self.get_ts(server, key, pts['ts'])
            if 'updates' not in pts:
                pts = self.get_long_poll()
                key = pts['key']
                server = pts['server']
            else:
                self.middleware(pts['updates'])

    def long_poll(self):
        """
        Инициализация и запуск процесса LongPoll
        :return:
        """
        thread = threading.Thread(target=self.init_long_poll)
        thread.start()
        self.logger.log('Long pull запущен')

    def middleware(self, items):
        """
        Обработчик поступающих событий
        :param items:
        :return:
        """
        if items is not None:
            for item in items:
                thread = threading.Thread(target=self.thread_object, args=[self.is_command, item])
                thread.start()

    def handler_signal(self, signal_proc, frame):
        """
        Уничтожение процесса
        :param signal_proc:
        :param frame:
        :return:
        """
        pid = os.getpid()
        os.kill(pid, signal.SIGKILL)

    def register_commands(self, *commands):
        """
        Регистрация комманд
        :param commands:
        :return:
        """

        for cmd in commands:
            command = cmd()
            self.commands.append({'name': command.name, 'event': command.event,
                                  'result': command.result, 'filter': command.filter})

    def register_symbol_command(self, symbol):
        """
        Регистрация символа команды
        :param symbol:
        :return:
        """
        self.symbol_command = symbol

    def register_symbol_answer(self, symbol):
        """
        Регистрация символа ответа
        :param symbol:
        :return:
        """
        self.symbol_answer = symbol

    def is_command(self, item):
        """
        Проверка: является ли сообщение командой
        :param item:
        :return:
        """
        for cmd in self.commands:
            event = item['type']

            if event == cmd['event']:
                if cmd['filter'](item['object'], self.symbol_command, self.symbol_answer):
                    resposne = cmd['result'](self, item)
                    if resposne:
                        self.replay(resposne, item)

    def replay(self, text, item):
        """
        Ответ, если он предусмотрен командой
        :param text:
        :param item:
        :return:
        """
        peer_id = item['object']['peer_id']
        random_id = random.randint(11111111111, 99999999999)
        message = text
        self.query('messages.send', {'peer_id': peer_id, 'random_id': random_id, 'message': message,
                                     'group_id': self.options['group_id']})

    def timeout(self):
        """
        Функция реализации таймаута
        :return:
        """
        return self.options['max_timeout']

    @staticmethod
    def thread_object(cmd, *args):
        """
        Объект потока
        :param cmd:
        :param args:
        :return:
        """
        cmd(*args)
        exit()

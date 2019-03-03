from vk_api.logger import Logger


class Tokenizer:
    def __init__(self, name, api):
        self.name = name
        self.api = api
        self.logger = Logger('tokenizer')

    def check_token_file(self):
        """
        Проверка, существует ли файл с токеном
        :return:
        """
        try:
            with open(self.name, 'r', encoding='utf-8'):
                return True
        except FileNotFoundError:
            self.api.login()
            token = open(self.name, 'w', encoding='utf-8')
            token.write(self.api.token)
            token.close()
            return False

    def check_valid_file(self):
        """
        Проверяет есть ли в файле что-то похожее на токен
        :return:
        """
        token = open(self.name, 'r', encoding='utf-8')
        if len(token.read()) > 60:
            token.seek(0)
            self.api.token = token.read()
            token.close()
            return True
        else:
            self.api.login()
            token = open(self.name, 'w', encoding='utf-8')
            token.write(self.api.token)
            token.close()
            return False

    def token_init(self):
        """
        Инициирует процедуру проверки токена
        :return:
        """
        if self.check_token_file() and self.check_valid_file():
            self.logger.log('Токен получен')
        else:
            self.logger.log('Авторизация успешна. Токен записан')

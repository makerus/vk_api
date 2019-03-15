# vk_api
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Библиотека для работы с API социальной сети ВКонтакте на Python.

```python
pip install vk-api-boroda34
```

```python
from vk_api.core.api import VkApi

# Инициализация объекта VK API для пользователя
api = VkApi.login({
    'client_id': config.CLIENT_ID,
    "scope": config.SCOPE,
    "api_v": config.VERSION_API,
    "login": config.LOGIN,
    "password": config.PASSWORD,
    "max_timeout": config.MAX_TIMEOUT
})

# Инициализация объекта VK API для группы
bot = VkApi({
    'client_id': config.CLIENT_ID,
    'scope': config.SCOPE_GROUP,
    'api_v': config.VERSION_API,
    'token': config.TOKEN_GROUP,
    'max_timeout': config.MAX_TIMEOUT,
    'group_id': config.GROUP_ID
})

# Авторизация и получение токена
api.get_token(api)

# Опциональные команды

# Инициализация команд
api.register_commands(ClassName)
# Регистрация символа команды
api.register_symbol_command('#')
# Регистрация символа ответа
api.register_symbol_answer('!')

# Работа longPool (запускает отдельный поток)
api.long_poll()

```

Для работы библиотеки потребуется файл ```config.py```
Содержание этого файла должно быть следующим:
```python
CLIENT_ID = 000000  # ID приложения
VERSION_API = "5.92"  # Версия API
LEVEL_LOG = 0  # Уровень ошибок 0 - ВСЕ, 1 - ТОЛЬКО INFO и ERRORS, 2 - ТОЛЬКО ERRORS
MAX_TIMEOUT = 3  # Таймаут в 3 секунды

# Для пользоавтеля
SCOPE_USER = "friends,photos,video,status,wall,offline,docs,groups"  # Здесь указаны права доступа
LOGIN = ""  # Номер телефона или email от профиля бота
PASSWORD = ""  # Пароль от профиля бота

# Для группы
TOKEN_GROUP = ""  # токен
SCOPE_GROUP = "stories,photos,app_widget,messages,docs,manage"  # Здесь указаны права доступа
GROUP_ID = 000000
```
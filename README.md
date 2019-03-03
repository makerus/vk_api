# vk_api
Библиотека для работы с API социальной сети ВКонтакте на Python

```python
pip install vk-api-boroda34
```

```python
from vk_api.core.api import VkApi

api = VkApi.login({
    'client_id': config.CLIENT_ID,
    "scope": config.SCOPE,
    "api_v": config.VERSION_API,
    "login": config.LOGIN,
    "password": config.PASSWORD,
    "max_timeout": config.MAX_TIMEOUT
})
```

Для работы библиотеки потребуется файл ```config.py```
Содержание этого файла должно быть следующим:
```python
CLIENT_ID = ''  # ID приложения
SCOPE = 'friends,photos,video,status,messages,wall,offline,docs,groups'  # Здесь указаны права доступа
LOGIN = ''  # Номер телефона или email от профиля бота
PASSWORD = ''  # Пароль от профиля бота
VERSION_API = '5.92'  # Версия API
LEVEL_LOG = 0  # Уровень ошибок 0 - ВСЕ, 1 - ТОЛЬКО INFO и ERRORS, 2 - ТОЛЬКО ERRORS
MAX_TIMEOUT = 3 # Время таймаута (время отправки запросов к API ВКонтакте) в секундах

```
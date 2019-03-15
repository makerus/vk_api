from setuptools import setup, find_packages

setup(name='vk_api_boroda34',
      version='0.2.3',
      description='Библиотека для работы с API социальной сети ВКонтакте',
      author='boroda34',
      url='https://github.com/makerus',
      keywords='vk api вк вконтакте апи vk.com',
      install_requires=[
          'requests',
          'beautifulsoup4',
          'utils',
          'gevent'
      ],
      license='MIT',
      packages=find_packages())

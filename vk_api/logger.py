from datetime import datetime
import config


class Logger:
    def __init__(self, meta):
        self.meta = meta
        self.level_log = config.LEVEL_LOG

    def log(self, text):
        """
        Обычное логирование
        :param text:
        :return:
        """
        if self.level_log < 2:
            output = "[" + self.meta + "]" + \
                     "[" + str(datetime.strftime(datetime.now(), "%x %H:%M")) + "] LOG: " + str(text) + "..."
            log_info = open("logs/info.log", 'a', encoding="utf-8")
            log_info.write(output + '\n')
            log_info.close()
            print(output)

    def error(self, text):
        """
        Логирование ошибок
        :param text:
        :return:
        """
        output = "[" + self.meta + "]" + \
                 "[" + str(datetime.strftime(datetime.now(), "%x %H:%M")) + "] ERROR: " + str(text) + "..."
        log_error = open("logs/error.log", 'a', encoding="utf-8")
        log_error.write(output + '\n')
        log_error.close()
        print(output)

    def debug(self, text):
        """
        Отладочная инфорамция
        :param text:
        :return:
        """
        if self.level_log == 0:
            output = "[" + self.meta + "]" + \
                     "[" + str(datetime.strftime(datetime.now(), "%x %H:%M")) + "] DEBUG: " + str(repr(text)) + "..."
            log_debug = open("logs/debug.log", 'a', encoding="utf-8")
            log_debug.write(output + '\n')
            log_debug.close()
            print(repr(output))

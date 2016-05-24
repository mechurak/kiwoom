import logging


class Singleton:
    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__get_instance
        return cls.__instance


class MyLogger(Singleton):
    def __init__(self):
        self._logger = logging.getLogger("PyStock")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s (%(funcName)s) %(message)s')

        filename = 'my_log.log'
        #fileMaxByte = 10 * 1024 * 1024 * 100  # 10MB
        #fileHandler = logging.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10)
        fileHandler = logging.FileHandler(filename)
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

    def logger(self):
        return self._logger

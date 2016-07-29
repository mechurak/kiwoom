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

        log_dir = "log"
        import os
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        from datetime import date
        today = date.today()
        filename = log_dir + "/" + today.strftime("%Y%m%d") + ".log"

        fileHandler = logging.FileHandler(filename, "a", "utf-8")
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

    def logger(self):
        return self._logger

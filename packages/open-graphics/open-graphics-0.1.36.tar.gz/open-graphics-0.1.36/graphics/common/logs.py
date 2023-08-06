import logging


class Logger:

    def __init__(self):
        logger = logging.getLogger('console')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        log_format = '%(asctime)s  %(levelname)s %(process)d --- [%(threadName)+15s] %(module)-20s : %(message)s'
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S.000')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger


logs = Logger().logger

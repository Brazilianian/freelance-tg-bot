import logging

FILE_PATH = './log/.log'


def init_logger():
    logging.basicConfig(filename=FILE_PATH,
                        filemode='a',
                        encoding='utf-8',
                        format='%(asctime)s: [%(levelname)s] - %(message)s',
                        level=logging.INFO)

    pass

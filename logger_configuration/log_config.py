import logging
import os

DIRECTORY_PATH = './log/'
FILE_PATH = '.log'


def init_logger():
    if not os.path.exists(DIRECTORY_PATH):
        os.makedirs(DIRECTORY_PATH)

    full_file_path = DIRECTORY_PATH + FILE_PATH
    if not os.path.exists(full_file_path):
        with open(full_file_path, 'w'):
            pass

    logging.basicConfig(filename=full_file_path,
                        filemode='a',
                        encoding='utf-8',
                        format='%(asctime)s: [%(levelname)s] - %(message)s',
                        level=logging.INFO)

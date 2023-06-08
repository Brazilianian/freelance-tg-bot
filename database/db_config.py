import configparser

from peewee import *

config = configparser.ConfigParser()
config.read('db.ini')

db = MySQLDatabase(
    host=config["tg"]["host"],
    database=config["tg"]["name"],
    user=config["tg"]["user"],
    password=config["tg"]["password"]
)

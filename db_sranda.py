import json
import csv
import configparser
from pprint import pprint 

from database_adapter import Database


config = configparser.ConfigParser()
config.read('db_config.ini')
db = Database(config['DB'])
db_test = db.expose('PC6_sysmon')

items = []

for item in db_test.find({}, {"Message.Image": 1, "_id": 0}):
	try:
		items.append(item['Message']['Image'])
	except KeyError:
		pass

pprint(set(items))
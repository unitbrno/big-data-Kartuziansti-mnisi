import json
import csv
from pprint import pprint
import configparser

from database_adapter import Database

config = configparser.ConfigParser()
config.read('db_config.ini')
db = Database(config['DB'])


with open('./csv/ufw_short.log', newline='') as csvfile:
	
	data = []
	cnt = 0

	for item in csvfile:
		new_item = {}

		# general info
		new_item["info"] = item.split(" ")[:8]

		# only key-value data (from 8 positon)
		for i in item.split(" ")[8:-1]:
			tmp = i.split("=")
			try:
				new_item[tmp[0]] = int(tmp[1])
			except IndexError:
				pass
			except:
				new_item[tmp[0]] = tmp[1]

		# if cnt > 10:
		# 	break

		cnt += 1
		

		db.post('FIREWALL', new_item)
		#pprint(new_item)
		data.append(new_item)

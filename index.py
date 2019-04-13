import json
import csv
import configparser

from database_adapter import Database


config = configparser.ConfigParser()
config.read('db_config.ini')
db = Database(config['DB'])

with open('PC1_security.csv', newline='') as csvfile:
	csv_reader = csv.reader(csvfile, delimiter=';')
	cnt = 0

	header = []
	data = []

	for item in csv_reader:
		"""
		Get header
		"""
		if cnt == 0:
			header = item
		else:
			if item:
				new_item = {}
				for it, data_item in enumerate(item):
					new_item[header[it]] = data_item
				db.post('PC1_security', new_item)


		# if cnt > 10:
		#  	break

		cnt += 1

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
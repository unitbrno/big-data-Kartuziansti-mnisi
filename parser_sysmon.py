import json
import csv
from pprint import pprint



with open('../csv/PC1_sysmon.csv', newline='') as csvfile:
	csv_reader = csv.reader(csvfile, delimiter=';')
	
	cnt = 0

	header = []
	data = []

	for item in csv_reader:

		if cnt == 0:
			header = item
		else:
			if item:
				new_item = {}
				for it, data_item in enumerate(item):
					if header[it] == "Message":
						message = {}
						msg = data_item.split("\r\n")

						for i in msg:
							msg_item = i.split(":")
							message[msg_item[0]] = str.join(':', msg_item[1:])
						new_item[header[it]] = message
					else:
						new_item[header[it]] = data_item
				#db.post('PC1_security', new_item)
				pprint(new_item)


		if cnt > 10:
		 	break

		cnt += 1

"""
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)"""
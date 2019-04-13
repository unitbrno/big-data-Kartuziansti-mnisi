"""
Systemove knihovny
"""
import json
import csv
import configparser
from pprint import pprint 
import sys
from termcolor import colored
import datetime
import re
"""
Vlastni moduly
"""
from database_adapter 	import Database
import utils			as utils
"""
Konfigurace databaze
"""
config = configparser.ConfigParser()
config.read('db_config.ini')
db = Database(config['DB'])
"""
Pocitace, lze rozsirit dynamicky, zde jasne zadan pocet
pro zjednoduseni pridano manualne.
Automaticky doplnime IP
"""
COMPUTERS = {
	'PC1': '',
	'PC2': '',
	'PC5': '',
	'PC6': ''
}

for computer_id in COMPUTERS:
	print(computer_id)

	db_security = db.expose('{}_security'.format(computer_id))
	pprint(db_security.find_one({}, {"Message.Source Address": 1, "_id": 0}))










# regx = re.compile("^10\\.", re.IGNORECASE)
# for item in db_security.find({"Message.Destination Address": regx}):
# 	pprint(item)
# 	print('\n\n')

for item in db_security.find({"Message.Source Address": '10.32.128.68'}):
	pprint(item)


# items = []
# for item in db_security.find({}, {'_id': 0, 'Message.Process ID': 1}):
# 	try:
# 		item['Message']
# 		try:
# 			items.append(item['Message']['Process ID'])
# 		except KeyError:
# 			pass
# 	except KeyError:
# 		pass
# 	except ValueError:
# 		pass

# pprint(set(items))

#db.PC1_security.find({},{"Message.Process ID": 1, "_id": 0}).pretty()
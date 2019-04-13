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
Nastavime informace o firewallu
"""
FIREWALL = {
	'addresses': [
		'192.168.50.254',
		'192.168.56.254'
	]
}

utils.msg_info('test check', 'Checking firewall with IP addresses:\n{}'.format(FIREWALL['addresses']))
utils.msg_divider()


CLIENTS = {
	'LAN_network': [
		'192.168.50.101',
		'192.168.50.102',
		'192.168.50.105',
		'192.168.50.106',
	],
	'MNG_network': [
		'192.168.56.1',
		'192.168.56.50'
	]
}
"""
U Firewallu se nachazi moznost sdilet soubory
pres SAMBU, ktera by urcite nemela nic vysilat
"""
VULNERABLE_SERVICES = {
	'445' 	: 'SAMBA',
	'137'	: 'NETBIOS'
}
vulnerable_devices = []
"""
Vezmeme vsechny IP a podivame se, jestli nahodou 
nejsou cile vysilani Firewallu
"""
all_clients = []
for subnet in CLIENTS:
	[all_clients.append(_) for _ in CLIENTS[subnet]]
"""
Vysetreni komunikace Firewallu
"""
db_firewall = db.expose('FIREWALL')
for item in db_firewall.find(
	{'SRC': {'$in': FIREWALL['addresses']}, 'DST': {'$in': all_clients}}, 
	{'_id': 0}):

	if item['DST'] not in vulnerable_devices:
		vulnerable_devices.append(item['DST'])


if vulnerable_devices:
	utils.msg_error('test check', 'Firewall used as source for messages,\nnot intended behaviour')

for device in vulnerable_devices:
	utils.msg_info('vulnerability', '{}'.format(item['DST']))


#print(vulnerable_devices)
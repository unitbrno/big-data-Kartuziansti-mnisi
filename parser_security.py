import json
import csv
import configparser
from pprint import pprint 
import sys
from termcolor import colored
import datetime

from database_adapter 	import Database
import utils			as utils


config = configparser.ConfigParser()
config.read('db_config.ini')
db = Database(config['DB'])

def retype_date(val):
	return [int(x) for x in val]

def parse_date(item, string_date):
	date, time = string_date.split(' ')[:2]
	"""
	Parse individual items
	"""
	if item == 'UtcTime':
		year, month, day 		= retype_date(date.split('-'))
		time, millis			= time.split('.')
		hour, minute, second	= retype_date(time.split(':'))
		millis 					= int(millis)

		#print(colored('UTC', 'cyan'))
		#print(year, month, day, hour)
		return utils.number_from_date(year, month, day, hour, minute, second, millis) + (millis / 1000)
	
	elif item == 'TimeCreated':
		if date.find('/') == -1:
			day, month, year		= retype_date(date.split('.'))
		else:
			month, day, year		= retype_date(date.split('/'))

		hour, minute, second	= retype_date(time.split(':'))

		#print(colored('Time', 'green'))
		#print(year, month, day, hour)
		return utils.number_from_date(year, month, day, hour, minute, second)

with open('./csv/{}.csv'.format(sys.argv[1]), newline='') as csvfile:
	csv_reader = csv.reader(csvfile, delimiter=';', lineterminator='"System.Collections.Generic.List`1[System.Diagnostics.Eventing.Reader.EventProperty]"')
	cnt = 0

	header = []
	data = []
	len_data = []
	len_keys = []

	#string = csvfile.read()
	#print()

	# for item in string.splitlines():
	# 	print(item)
	# print(string.index('"System.Collections.Generic.List`1[System.Diagnostics.Eventing.Reader.EventProperty]"'))


	# with open('somefile.txt', 'a') as the_file:
	#  	the_file.write("".join(string.split()))

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
					prepared_item = data_item if data_item else None
					"""
					Pretypovani pro cisla
					"""
					try:
						prepared_item = float(prepared_item)
					except ValueError:
						pass
					except TypeError:
						pass

					"""
					Vyresit datum a pridat jako polozku do DB
					"""
					if header[it] == 'TimeCreated':
						prepared_item = parse_date('TimeCreated', prepared_item)
					new_item[header[it]] = prepared_item

				#pprint(new_item)
				#print(colored(cnt, 'red'))
				#print(item[-1])
				len_data.append(item[-1])
				len_keys.append(len(new_item.keys()))


				mess_items = new_item['Message']
				filtered_items = {}

				
					
				utils.msg_info('test', cnt)
				for n_item in mess_items.split(' '):
					try:
						exe_index = n_item.index('.exe')
						indxx = n_item.strip().index('\r')
						print(n_item[:indxx])
					except ValueError:
						pass


				#print(mess_items.strip())
				

				
				
				#print('')

				# # print(mess_items)
				# # print()

				# for it, itm in enumerate(mess_items):
				#  	if itm:
				#  		"""
				#  		Zahod vsechny redundatni znaky
				#  		"""
				#  		temp = itm.strip().replace('\t', '') if itm.strip() else None
				#  		"""
				#  		Pokud ma smysl pridavat do databaze
				#  		"""
				#  		if temp:
			 # 				double_dot_index = temp.find(':')
			 # 				if double_dot_index != -1:
				#  				key = temp[:double_dot_index].strip().replace('.', '_')
				#  				value = temp[double_dot_index+1:].strip()
				#  				"""
				#  				Prvni polozka, oznaceni zpravy, neni nutno upravovat
				#  				"""
				#  				if it:
				#  					if value:

				#  						try:
				# 	 						filtered_items[key] = float(value)
				# 	 					except ValueError:
				# 	 						filtered_items[key] = value
				# 	 					except TypeError:
				# 	 						filtered_items[key] = value

				# 	 					if key == 'UtcTime':
				#  							filtered_items[key] = parse_date('UtcTime', value)
				#  							#print('')



				new_item['Message'] = filtered_items if filtered_items else None
				#print(new_item)
				#db.post('{}'.format(sys.argv[1]), new_item)

		# if cnt > 100:
		#   	break

		cnt += 1

	if len(set(len_keys)) + len(set(len_data)) != 2:
		print('pruser')
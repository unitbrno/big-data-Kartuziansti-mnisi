"""
Prace s databazi - nerelacni (soucasne MongoDB)
@project: IBT19 - xmitas02
@brief: Prace s databazi - nerelacni (soucasne MongoDB)
@author: Matej Mitas
@file: ibt19_database.py
"""

import pymongo

class Database:
	# TODO: toz nejaky error handling by to chtelo, ni?
	# TODO: timeout pro neexistujici spojeni s DB
	def __init__(self, info):
		self.ok = True
		if (info['driver'] == 'mongodb'):
			try:
				self.client = pymongo.MongoClient(info['login'], int(info['port']), serverSelectionTimeoutMS=1000)
				self.db = self.client[info['database']]
				testing_collection = self.db['test']
				for item in testing_collection.find({}):
					print(item)
			except pymongo.errors.ServerSelectionTimeoutError:
				self.ok = False
		else:
			pass

	def check_connection(self):
		return self.ok

	def expose(self, collection):
		return self.db[collection]

	def get(self, collection, query, projection):
		return self.db[collection].find_one({}, projection if projection else None)

	def get_many(self, collection, query, projection):
		for item in self.db[collection].find(query, projection if projection else None):
			yield item

	def post(self, collection, payload):
		if not self.db[collection].insert_one(payload).inserted_id:
			return False
		return True

	def delete(self, collection, query):
		self.db[collection].delete_one(query);

	def delete_many(self, collection, query):
		self.db[collection].delete_many(query);
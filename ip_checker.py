import requests
import sys

"""
Udaje pro API
"""
headers = {
    'Key': 'df38b010fa020e9c20ba4702956c1495c3bbdfb9590afb329dae20f3a3ba6d9102f35c37cf9f4d4f',
    'Accept': 'application/json',
    'ipAddress': '118.25.6.39'
}

"""
Wrapper pro IP polozku
"""
ip_data = {
	'country'				: '',
	'isWhitelisted'			: False,
	'abuseConfidenceScore'	: []
}

"""
Zpracovani polozky
"""
def get_ip_info(val):
	try:
		address = val
		response = requests.post('https://www.abuseipdb.com/check/{}/json?key=df38b010fa020e9c20ba4702956c1495c3bbdfb9590afb329dae20f3a3ba6d9102f35c37cf9f4d4f&days=5'.format(address))
		for data in response.json():

			ip_data['isWhitelisted'] = data['isWhitelisted']
			ip_data['country'] = data['country']
			ip_data['abuseConfidenceScore'].append(data['abuseConfidenceScore'])

		ip_data['abuseConfidenceScore'] = sum(ip_data['abuseConfidenceScore'] / len(ip_data['abuseConfidenceScore']))
		print(ip_data)

	except KeyError:
		print('API nefunguje')

"""
Zpracovani souboru s IP adresami oddelenym 
"""
try:
	ips_list = []
	with open(sys.argv[1], 'r') as ip_file:
		ips_list = ip_file.read().split('\n')[:10]

	for it, ip in enumerate(ips_list):
		item = ip.split("'")[1]
		get_ip_info(item)

except IndexError:
	print('Dodejte soubor s IP adresami')





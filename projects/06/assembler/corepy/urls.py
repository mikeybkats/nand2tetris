#!/usr/bin/env python3
import sys

# strings numbers and tupls can be keys
# order of pairs is not definite
# dictionary can be created with dict()

def create_url_dictionary():
	global urls
	urls = dict([
		('google', 'http://google.com'),
		('pluralsight', 'http://pluralsight.com'),
		('sixty north', 'http://sixty-north.com'),
		('microsoft', 'http://microsoft.com')
		])

def update_url_dictionary(newValue):
	urls.update(newValue)

def check_if_url_exists(urlVal):
	if urlVal in urls.values():
		print("Url is present.")
		return True
	else:
		print("Url is not present.")
		return False

def print_url_vals():
	for urlVal in urls.values():
		print(urlVal)

def print_url_keys():
	for urlKey in urls.keys():
		print(urlKey)

def print_url_items():
	for urlItem in urls.items():
		print(urlItem)

def getUrl(name):
	return urls.get(name);

def createUrlSet():
	p = {10,20, 30, 40, 50}
	setP = set(p)

def main():
	create_url_dictionary()
	print_url_vals()
	update_url_dictionary({'hello deary': "https://hellodeary.com"})
	print(getUrl("hello deary"))
	print_url_keys()
	print_url_items()
	check_if_url_exists("https://hellodeary.com")
	check_if_url_exists("https://woot.com")

if __name__ == '__main__':
	main()

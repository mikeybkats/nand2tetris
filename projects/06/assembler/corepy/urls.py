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

def print_urls():
	for urlVal in urls.values():
		print(urlVal)
	# for url in urls:
	# 	print(urls[url])

def getUrl(name):
	return urls.get(name);

def main():
	create_url_dictionary()
	print_urls()
	update_url_dictionary({'hello deary': "https://hellodeary.com"})
	print(getUrl("hello deary"))

	

if __name__ == '__main__':
	main()

#!/usr/bin/env python3
# called shebang

# using script in mac os command:
# $ chmod +x filename 
# will make the script executable from the command line

import sys
from urllib.request import urlopen

def fetch_words(url='http://sixty-north.com/c/t.tx'):
	"""Fetch a list of words from a URL.
	Args:
		string url
	Returns:
		list of words
	"""
	story = urlopen(url)
	story_words=[]
	for line in story:
		line_words = line.decode('utf-8').split()
		for word in line_words:
			story_words.append(word)
	story.close()

	return story_words

def print_items(story_items):
	for item in story_items:
		print(item)

def main(url):
	words = fetch_words(url)
	print_items(words)

# double underscore is called dunder
if __name__ == '__main__':
	# see python arg parse module for more sophisticated arg parsing
	url = sys.argv[1] # The 0th arg is the module filename
	main(url)
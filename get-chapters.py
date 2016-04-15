#!/usr/bin/python
from lxml import html
import requests
import sys
import argparse

def GetMangaChapters(argv):
	# define input arguments
	parser = argparse.ArgumentParser(description='Get chapter count from http://www.mangareader.net/')
	parser.add_argument('-m', '--manga', required=True, action='store', nargs=1, type=str, help='A string agrument for the name of the manga. Should be taken from the url in http://mangareader.net')
	# parse input aruments
	argv = parser.parse_args(argv)
	manga = argv.manga[0]

	# find if manga exists
	page = requests.get('http://www.mangareader.net/' + manga)
	if len(page.text) < 100 or page.text.find("404 Not Found") > 0:
		print "\"" + manga + "\" cannot be found on the server."
		return()
	tree = html.fromstring(page.text)
	chapterList = tree.get_element_by_id('listing')
	for chapter in chapterList.getchildren():
		if chapter[0].values() == []:
			a = chapter[0].getchildren()[1].values()[0]
			print a.split("/")[1] + "   " + a.split("/")[2]

	return

if __name__ == "__main__":
	GetMangaChapters(sys.argv[1:])


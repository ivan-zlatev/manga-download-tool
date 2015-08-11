#!/usr/bin/python
from lxml import html
import requests
import os
import zipfile
import sys
import argparse
from glob import glob

def DownloadMangaTool(argv):

	parser = argparse.ArgumentParser(description='Download some manga.')
	parser.add_argument('-s', '--start', required=True, action='store', nargs=1, type=int, help='An integer argument for first chapter to download.')
	parser.add_argument('-f', '--finish', required=True, action='store', nargs=1, type=int, help='An integer argument for last chapter to download.')
	parser.add_argument('-m', '--manga', required=True, action='store', nargs=1, type=str, help='A string agrument for the name of the manga to be downloaded. Should be taken from the url in http://mangareader.net')
	parser.add_argument('-p', '--path', action='store', nargs=1, type=str, default=[ os.path.expanduser('~') + '/download-manga'], help='An optional string argument for download path. If not given, the manga will be downloaded at ' + os.path.expanduser('~') + '/download-manga/<MANGA>')
	parser.add_argument('-g', '--group', action='store', nargs=1, type=int, default=[5], help='An optional argument for grouping the downloaded chapter in cbz archives. If not given, the manga will be grouped in 5 chapter archives.')
	parser.add_argument('-c', '--clear', action='store_true', help='An optional argument for clearing the images after grouping in cbz archives.')
	argv = parser.parse_args(argv)
	start = argv.start[0]
	finish = argv.finish[0]
	manga = argv.manga[0]
	path = argv.path[0]
	group = argv.group[0]
	clear = argv.clear
	if start > finish:
		print "Finish chapter should be the same or higher than start chapter."
		return()
	chapters = []
	pages = []
	path = path + '/' + manga
	page = requests.get('http://www.mangareader.net/' + manga + '/' + str(start) + '/1')
	if len(page.text) < 100 or page.text.find("is not released yet") > 0:
		print "\"" + manga + "\" chapter " + str(start) + " cannot be found on the server."
		return()
	if not os.path.exists(path):
		os.makedirs(path)
	path = path + "/" + manga
	# get a list of all chapters and their pages
	for i in range( int(start), int(finish)+1):
		page = requests.get('http://www.mangareader.net/' + manga + '/' + str(i))
		if len(page.text) < 100 or page.status_code == 404:
			print "\"" + manga + "\" cannot be found on the server."
		else:
			if page.text.find("is not released yet") < 0:
				tree = html.fromstring(page.text)
				for option in tree.cssselect('select'):
					if option.name == 'pageMenu':
						for tmp in option.getchildren():
							pages.append([i, tmp.items()[0][1]])
				chapters.append(pages)
				pages = []
			else:
				print "Chapter " + str(i) + " is not released yet."
	if chapters == []:
		print "No chapters found for download."
		return()
	manga = []
	manga_page = []
	manga_chapter = []
	tmp_chap = 0
	tmp_page = 0
	# get a list of all img urls
	for tmp in chapters:
		print "Downloading information about chapter " + str(tmp[0][0])
		for tmp2 in tmp:
			if len(tmp2[1].split('/')) == 4:
				tmp_chap = tmp2[1].split('/')[2]
				tmp_page = tmp2[1].split('/')[3]
			elif len(tmp2[1].split('/')) == 3:
				tmp_chap = tmp2[1].split('/')[2]
				tmp_page = '1'
			page = requests.get('http://www.mangareader.net' + tmp2[1])
			tree = html.fromstring(page.text)
			for tmp3 in tree.cssselect('img'):
				for tmp4 in tmp3.items():
					if tmp4[0] == 'src':
						manga_page.append([str( "%.5d" % int(tmp_chap) ), str( "%.5d" % int(tmp_page)), tmp4[1]])
			manga_chapter.append(manga_page[0])
			manga_page = []
		manga.append(manga_chapter)
		manga_chapter = []
	i = 0
	tmp = []
	tmp_chap1 = 0
	tmp_chap2 = 1
	#download and rename everything
	for chap in manga:
		print "Downloading chapter " + str(int(chap[0][0]))
		for page in chap:
			f = open(path + page[0] + page[1] + "." + page[2].split('.')[-1:][0], "wb")
			f.write(requests.get(page[2]).content)
			f.close()

			tmp.append(str(path + page[0] + page[1] + "." + page[2].split('.')[-1:][0]))
		if i == 0:
			tmp_chap1 = chap[0][0]
		tmp_chap2 = chap[0][0]
		i += 1
		if i%group == 0 or int(finish)-int(start) == 0 or i%(int(finish)-int(start)) == 0:
			zipf = zipfile.ZipFile(str(path + tmp_chap1 + "-" + tmp_chap2 + ".cbz"), 'w')
			print(str(path + tmp_chap1 + "-" + tmp_chap2 + ".cbz") + " created")
			for img in tmp:
				zipf.write(img, arcname = img.split('/')[-1:][0] )
			zipf.close()
			i = 0
			tmp = []
			if clear:
				for img in glob(path + '*.jpg'):
					os.remove(img)

if __name__ == "__main__":
	DownloadMangaTool(sys.argv[1:])


#!/usr/bin/python
from lxml import html
import requests
import os
import zipfile
import sys

def main( start, finish, manga, path):
	chapters = []
	pages = []
	path = path + manga
	if not os.path.exists(path):
		os.makedirs(path)
	path = path + "/" + manga
	for i in range( int(start), int(finish)+1):
		page = requests.get('http://www.mangareader.net/' + manga + '/' + str(i))
		tree = html.fromstring(page.text)
		for option in tree.cssselect('select'):
			if option.name == 'pageMenu':
				for tmp in option.getchildren():
					pages.append([i, tmp.items()[0][1]])
		chapters.append(pages)
		pages = []
	manga = []
	manga_page = []
	manga_chapter = []
	tmp_chap = 0
	tmp_page = 0
	for tmp in chapters:
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
	for chap in manga:
		for page in chap:
			f = open(path + page[0] + page[1] + "." + page[2].split('.')[-1:][0], "wb")
			f.write(requests.get(page[2]).content)
			f.close()
			print(str(path + page[0] + page[1] + "." + page[2].split('.')[-1:][0]))
			tmp.append(str(path + page[0] + page[1] + "." + page[2].split('.')[-1:][0]))
		if i == 0:
			tmp_chap1 = chap[0][0]
		tmp_chap2 = chap[0][0]
		i += 1
		if i%5 == 0 or i%(int(finish)-int(start)) == 0:
			zipf = zipfile.ZipFile(str(path + tmp_chap1 + tmp_chap2 + ".cbz"), 'w')
			print(str(path + tmp_chap1 + tmp_chap2 + ".cbz") + " created")
			for img in tmp:
				zipf.write(img, arcname = img.split('/')[-1:][0] )
			zipf.close()
			i = 0
			tmp = []
main(sys.argv[1], sys.argv[2], sys.argv[3], '/home/izlatev/python_wd/other/')

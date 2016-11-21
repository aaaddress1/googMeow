#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-

from pyquery import PyQuery as pq
from lxml import etree
import requests
import urllib
import html2text

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36',
}

def printImportScreen(title, url, src, keyword):
	print '====================================='
	title = (title.encode('utf-8').replace(' ',''))[:50] + '...'
	print 'Found Keyword in the page "%s"' % (title)
	print 'URL: %s' % url
	print '====================================='

	h = html2text.HTML2Text()
	h.ignore_links  = True
	foundKey = False
	listCount = 0

	gg = h.handle(src)
	for i in gg.encode('utf-8').split('\n'):
		if keyword in i: foundKey = True
		if i == '\n': continue
		if foundKey: 
			listCount += 1
			if listCount > 10:
				break
			print i
	return

with open('logo.txt','r') as f: print f.read()
print '\n\nSearch >_',
question = raw_input()#'實際存放使用者密碼的檔案為下列何者'
d = pq(url='https://www.google.com.tw/search?&btnG=Google+Search&q=%s' % urllib.quote(question))

searchResultArr = d('.g')
for i in range(len(searchResultArr)):
	currItem = searchResultArr.eq(i)

	title = urllib.unquote(currItem.text())

	if currItem.find('li').eq(0):
		googleCachePath = (currItem.find('li').eq(0)).find('a').attr('href')
		googleCachePath = 'http://www.google.com%s' % googleCachePath
		src = requests.get(googleCachePath).text
		
		if question in src.encode("utf-8"):
			printImportScreen(title, googleCachePath, src, question)
			print '[按任意鍵繼續]'
			raw_input()
	else:
		pass
		#print 'there is no cache of %s.' % title
#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib2
import re
import shutil
import os

class CrawlerPgdoc():

    # SAVE_PATH = '/home/chenyarong/var/python/crawler/doc/'
    URL_PREFIX = 'http://www.postgres.cn/docs/9.6/'
    crawled_urls = []

    def __init__(self):
        self.SAVE_PATH = os.getcwd() + "/doc/"

    def dispatcher(self):
        pass
        

    # 循环抓取
    def crawlePage(self, url):
        if url in self.crawled_urls:
            return

        self.crawled_urls.append(url)
        # print url, "\n"

        prefixLen = len(self.URL_PREFIX)
        filename = url[prefixLen:]

        if not filename:
            filename = 'index.html'
        else:
            print filename

        html = self.fetchHtml(url)
        self.writeLocalFile(filename, html)
        uris = self.fetchHtmlUri(html)

        # 循环抓取
        for uri in uris:
            url = self.URL_PREFIX + uri
            self.crawlePage(url)


    # 抓取网页内容
    def fetchHtml(self, url):
        response = urllib2.urlopen(url)
        html = response.read()
    
        return html
    
    # 爬取html中的uri
    def fetchHtmlUri(self, html):
        pattern = "<A[\s\t\n]HREF=\"([^http].*\.html)\""
        uris = re.findall(pattern, html)
    
        if None == uris:
            return []
    
        return uris
    
    def writeLocalFile(self, filename, html):
        directory, name = os.path.split(filename)
        path = self.SAVE_PATH
        if directory:
            path = path + directory + '/'
            os.makedirs(path)

        print path + name, "\n"

        fp = open("tmp.html", "w")
        fp.write(html)
        fp.close()

        shutil.move("tmp.html", path + name)
        


crawler = CrawlerPgdoc()
crawler.crawlePage('http://www.postgres.cn/docs/9.6/')
# crawler.dispatcher()





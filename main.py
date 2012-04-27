#!/usr/bin/env python

import webapp2

import urllib
import hashlib
import re
from datetime import date
from bs4 import BeautifulSoup

import DataModel

import feedparser

feed_encoding = 'ISO-8859-1'

feed_url = 'http://feeds.feedburner.com/gameone'
main_site_url = 'http://www.gameone.de/'
blog_site_url = 'http://www.gameone.de/blog/'

main_link_find = '/blog/([0-9]{4})/([0-9]{1,2})/([a-zA-Z0-9_-]+)/?'
blog_link_find = 'href="([0-9]{4})/([0-9]{1,2})/([a-zA-Z0-9_-]+)/?"'

cur_year = date.today().year
cur_month = date.today().month

def printline(obj, data):
  obj.response.out.write(data + '<br>')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class TestHandler(webapp2.RequestHandler):
    def get(self):
        d = feedparser.parse(feed_url)
        for x in d.entries:
          try:
            name = x.title.encode(feed_encoding)
            url = x.link.encode(feed_encoding)

            if not DataModel.FeedEntry.all().filter('name =', name).get():
              new_entry = DataModel.FeedEntry(name=name, url=url)
              new_entry.restricted = urllib.urlopen(url).read()
              new_entry.put()

              printline(self, name)
          except:
            pass

        printline(self, '<br>success!')

class BlogLoaderHandler(webapp2.RequestHandler):
    def get(self):
      source_code = urllib.urlopen(blog_site_url).read()
      soup = BeautifulSoup(source_code)
      for item in soup.find_all('a', { "class" : "image_link" }):
        self.response.out.write(item.get('href'))
        self.response.out.write('<br>')


      self.response.out.write('<br>')
      self.response.out.write('<br>')


      source_code = urllib.urlopen(main_site_url).read()
      soup = BeautifulSoup(source_code)
      for item in soup.find_all('a', { "class" : "img_link" }):
        x = re.search(main_link_find,item.get('href'))

        if x == None:
          continue
        else:
          if (int(x.group(1)) == cur_year and int(x.group(2)) >= cur_month-1) or \
              cur_month == 1 and (int(x.group(2)) == 12 and int(x.group(1)) == cur_year-1):
            printline(self, 'http://www.gameone.de/blog/' + x.group(1) + '/' + x.group(2) + '/' + x.group(3))

class ParseHandler(webapp2.RequestHandler):
    def get(self):
      self.response.out.write('test')

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/test', TestHandler),
                               ('/url', BlogLoaderHandler),
                               ('/parse', ParseHandler)], debug=True)

#!/usr/bin/env python


import webapp2

import hashlib

import DataModel

import feedparser

feed_encoding = 'ISO-8859-1'

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')
        DataModel.BlogPost(url='http://google.de',name='test').put()

class TestHandler(webapp2.RequestHandler):
    def get(self):
        d = feedparser.parse("http://feeds.feedburner.com/gameone")
        for x in d.entries:
          try:
            self.response.out.write(x.title.encode(feed_encoding))
            self.response.out.write(x.link.encode(feed_encoding))
          except:
            self.response.out.write('Error at: ' + repr(x.title))

        self.response.out.write('success!')

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/test', TestHandler)], debug=True)

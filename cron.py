#!/usr/bin/env python

# Imports ###########################################################################
# ###################################################################################

import webapp2
import urllib
import hashlib
import re
import DataModel
import feedparser

from datetime import date
from bs4 import BeautifulSoup

# Constants
feed_encoding = 'ISO-8859-1'

main_feed_url = 'http://feeds.feedburner.com/gameone'
site_urls     = [('http://www.gameone.de/',      'img_link'),
                 ('http://www.gameone.de/blog/', 'image_link')]

regex_links = '/blog/([0-9]{4})/([0-9]{1,2})/([a-zA-Z0-9_-]+)/?'

# Cronjob handler ###################################################################
# ###################################################################################
class CronjobHandler(webapp2.RequestHandler):

    # crawl an RSS feed for new entries
    @staticmethod
    def crawlRssFeed(feed_url, type):
      # prase feed
      d = feedparser.parse(feed_url)

      for entry in d.entries:
        try:
          # get name and url
          name = entry.title.encode(feed_encoding)
          url = entry.link.encode(feed_encoding)
          # check if feed entry already exists -  based on rss entry name, which should!! be unique

          existing_entry = DataModel.FeedEntry.all().filter('name =', name).get()

          if existing_entry is None:
            new_entry = DataModel.FeedEntry(name=name, url=url)
          else:
            new_entry = existing_entry

          # save page content based on cronjob type for later comparison
          if type == 'restricted' and existing_entry is None:
            new_entry.restricted = urllib.urlopen(url).read()
            new_entry.put()

          elif type == 'unrestricted':
            new_entry.unrestricted = urllib.urlopen(url).read()
            new_entry.put()

        except:
          pass



    # crawl a Page and extract specific links using html parsing engine "BeautifulSoup"
    @staticmethod
    def crawlPage(page_url, link_class, type):
      source_code = urllib.urlopen(page_url).read()
      soup = BeautifulSoup(source_code)

      # dates to filter out old links during page crawl
      cur_year = date.today().year
      cur_month = date.today().month

      # get all links tagged with class: $link_class
      for item in soup.find_all('a', { "class" : link_class }):
        x = re.search(regex_links,item.get('href'))

        if x == None:
          continue
        else:
          if (int(x.group(1)) == cur_year and int(x.group(2)) >= cur_month-1) or \
              cur_month == 1 and (int(x.group(2)) == 12 and int(x.group(1)) == cur_year-1):
            pass #print(x.group(1) + '/' + x.group(2) + '/' + x.group(3))
            # todo



    # handle web (get) requestand perform
    def get(self, restricted_type):
        # fetch rss feed for new entries
        self.crawlRssFeed(main_feed_url, restricted_type)

        # fetch sites for brand new posts which are not yet in the rss feed
        #for site in site_urls:
          #self.crawlPage(site[0], site[1], restricted_type)

        self.response.out.write('Done!')


# Main handler ######################################################################
# ###################################################################################
app = webapp2.WSGIApplication([('/cron/crawl/(\w+)', CronjobHandler)], debug=True)
# ###################################################################################
# ###################################################################################
#!/usr/bin/env python

import datetime
from google.appengine.ext import db
from google.appengine.api import users


#class VideoEntry():
#  ordering = string
#  video_id = int


class BlogPost(db.Model):
  url      = db.LinkProperty(required=True)
  part     = db.IntegerProperty()
  name     = db.StringProperty(required=True)
  created  = db.DateTimeProperty(auto_now_add=True, required=True)

class FeedEntry(db.Model):
  name    = db.StringProperty(required=True)
  url     = db.LinkProperty(required=True)
  fetched = db.DateTimeProperty(auto_now_add=True, required=True)
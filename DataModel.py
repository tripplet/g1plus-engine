#!/usr/bin/env python

import datetime
from google.appengine.ext import db


#class VideoEntry():
#  ordering = string
#  video_id = int


class BlogPost(db.Model):
  url          = db.LinkProperty(required=True)
  part         = db.IntegerProperty()
  name         = db.StringProperty()
  created      = db.DateTimeProperty(auto_now_add=True, required=True)

# class for 
class FeedEntry(db.Model):
  name         = db.StringProperty(required=True,indexed=True)
  url          = db.LinkProperty(required=True,indexed=True)
  created      = db.DateTimeProperty(auto_now_add=True, required=True)
  restricted   = db.BlobProperty()
  unrestricted = db.BlobProperty()
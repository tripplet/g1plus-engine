#!/usr/bin/env python

import webapp2
import jinja2
import os
import hashlib
import DataModel

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):

      template_values = {
        'entries': DataModel.FeedEntry.all().order('-created').run(limit=25)
      }

      template = jinja_environment.get_template('main_template.html')
      self.response.out.write(template.render(template_values))

class BinaryDataHandler(webapp2.RequestHandler):
    def get(self, key, version):
      entry = DataModel.FeedEntry.get_by_id(int(key))

      if version == 'res':
        self.response.out.write(entry.restricted)
      elif version == 'unres':
        self.response.out.write(entry.unrestricted)


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/(\w+)_(\w+)', BinaryDataHandler)], debug=True)
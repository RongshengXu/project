__author__ = 'rongshengxu'
from google.appengine.api import users

import webapp2
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class OptionPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/option.html')
        self.response.write(template.render())

class OptionGet(webapp2.RequestHandler):
    def post(self):
        opt = self.request.get_all('options')[0]
        # self.response.write(opt)
        if opt == "order":
            self.redirect('/main')
        else:
            self.redirect('/main_restaurant')

app = webapp2.WSGIApplication([
    ('/option', OptionPage),
    ('/option_get',OptionGet)
], debug=True)
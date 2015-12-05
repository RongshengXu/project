from google.appengine.api import users

from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.ext import blobstore

import webapp2

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if (user):

            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'

            current_location = 'UT-Austin'              #get the current location in database

            template_values = {
                'user': user,
                'url': url,
                'url_linktext': url_linktext,
                'current_location': current_location,
            }
            template = JINJA_ENVIRONMENT.get_template('templates/main.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/main', MainPage)
], debug=True)
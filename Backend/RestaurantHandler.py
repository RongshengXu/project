from google.appengine.api import users

from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.ext import blobstore

import webapp2

import sys
import os
import jinja2
import json
from handlers.DataModel import RestaurantModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class EvaluatePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if (user):
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'

            template_values = {
                'user': user,
                'url': url,
                'url_linktext': url_linktext,
            }
            template = JINJA_ENVIRONMENT.get_template('templates/evaluate.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

class UserInfo(webapp2.RequestHandler):
    def get(self):
        comment = self.request.get('comment')
        userLogo = "http://www.gnosko.com/dist/img/unknown.gif"
        #userInfo = {"name": comment, "logo": userLogo}
        userInfo = {"name": users.get_current_user().nickname(), "logo": userLogo}

        # self.response.headers['Content-Type'] = 'application/json'
        userInfo_json = json.dumps(userInfo)
        self.response.write(userInfo_json)

app = webapp2.WSGIApplication([
    ('.*/evaluate', EvaluatePage),
    ('/getuserinfo', UserInfo)
], debug=True)

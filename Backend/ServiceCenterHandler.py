__author__ = 'rongshengxu'


from google.appengine.api import users
from handlers.DataModel import UserModel
import webapp2

import os
import jinja2
from handlers.DataModel import RestaurantModel, CartModel
import urllib

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ServiceCenterHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/servicecenter.html')
        template_values = {

        }
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/servicecenter', ServiceCenterHandler)
], debug=True)
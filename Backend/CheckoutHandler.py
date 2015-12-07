__author__ = 'rongshengxu'
from google.appengine.api import users
from handlers.DataModel import UserModel
import webapp2

import os
import jinja2
from handlers.DataModel import RestaurantModel, DishModel, OrderModel, CartModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CheckoutHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/checkout.html')

app = webapp2.WSGIApplication([
    ('/checkout', CheckoutHandler)
], debug=True)
__author__ = 'rongshengxu'
from google.appengine.api import users
from handlers.DataModel import UserModel
import webapp2

import os
import jinja2
import json
from handlers.DataModel import RestaurantModel, DishModel, OrderModel, CartModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CheckoutHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/checkout.html')

class DecrementHandler(webapp2.RequestHandler):
    def get(self):
        dish_name = self.request.get('dish_name')
        url = "/test?name=%s" % dish_name
        info = {"name": dish_name, "other": "hello"}
        info_json = json.dumps(info)
        self.response.write(info_json)
        # self.redirect(url)

class IncrementHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cart = CartModel.query(CartModel.user==user).fetch()[0]
        for order_key in cart.orders:
            order = order_key.get()

        dish_name = self.request.get('dish_name')
        url = "/test?name=%s" % dish_name
        info = {"name": dish_name, "other": "hello"}
        info_json = json.dumps(info)
        self.response.write(info_json)

class Test(webapp2.RequestHandler):
    def get(self):
        str = self.request.get('name')
        self.resposne.write(str)

app = webapp2.WSGIApplication([
    ('/checkout', CheckoutHandler),
    ('/decrement', DecrementHandler),
    ('/increment', IncrementHandler),
    ('/test', Test)
], debug=True)
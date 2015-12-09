__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

import os
import jinja2
import json
import urllib
from handlers.DataModel import RestaurantModel, DishModel, OrderModel, CartModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CheckoutHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/checkout.html')

class DecrementHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        dish_name = self.request.get('dish_name')
        restaurant_name = self.request.get('restaurant_name')
        id = int(self.request.get('id'))
        order = OrderModel.get_by_id(id)
        num = order.number
        if (num>0):
            cart = CartModel.query(CartModel.user==user, CartModel.restaurant_name==restaurant_name).fetch()[0]
            order.number = order.number - 1
            order.put()
            dish = order.dish.get()
            cart.total = cart.total - dish.price
            cart.put()
        info = {"name": dish_name, "other": restaurant_name, "id":id}
        info_json = json.dumps(info)
        self.response.write(info_json)
        # self.redirect(url)

class IncrementHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        dish_name = self.request.get('dish_name')
        restaurant_name = self.request.get('restaurant_name')
        id = int(self.request.get('id'))
        cart = CartModel.query(CartModel.user==user, CartModel.restaurant_name==restaurant_name).fetch()[0]
        order = OrderModel.get_by_id(id)
        order.number = order.number + 1
        order.put()
        dish = order.dish.get()
        cart.total = cart.total + dish.price
        cart.put()
        # url = "/test?name=%s" % dish_name
        info = {"name": dish_name, "other": restaurant_name, "id":id}
        info_json = json.dumps(info)
        self.response.write(info_json)

class CancelHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        restaurant_name = self.request.get('restaurant_name')
        id = int(self.request.get('id'))
        order = OrderModel.get_by_id(id)
        cart_query = CartModel.query(CartModel.restaurant_name==restaurant_name, CartModel.user==user).fetch()
        if (len(cart_query)>0):
            dish = order.dish.get()
            cart = cart_query[0]
            cart.orders.remove(order.key)
            cart.total = cart.total - order.number*dish.price
            cart.put()
            order.key.delete()
            p = urllib.urlencode({'name':restaurant_name})
            URL = '/viewsinglecart?%s' % p
            self.redirect(URL)
        else:
            self.redirect('/error')

class Test(webapp2.RequestHandler):
    def get(self):
        str = self.request.get('name')
        self.resposne.write(str)

app = webapp2.WSGIApplication([
    ('/checkout', CheckoutHandler),
    ('/decrement', DecrementHandler),
    ('/increment', IncrementHandler),
    ('/cancel', CancelHandler),
    ('/test', Test)
], debug=True)
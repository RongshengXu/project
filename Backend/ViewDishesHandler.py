__author__ = 'rongshengxu'

from google.appengine.api import users

import webapp2

from handlers.DataModel import RestaurantModel, DishModel, CartModel

import os
import jinja2
import urllib

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ViewDishHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        restaurant_name = self.request.get('name')

        # generate a cart
        cart_query = CartModel.query(CartModel.restaurant_name==restaurant_name, CartModel.user==user).fetch()
        if (len(cart_query)<1):
            cart = CartModel()
            cart.user = user
            cart.restaurant_name = restaurant_name
            cart.orders = []
            cart.total = 0
            cart.put()

        # self.response.write(restaurant_name)
        restaurant = RestaurantModel.query(RestaurantModel.name==restaurant_name, RestaurantModel.owner==user).fetch()[0]
        key = restaurant.key
        dish_query = DishModel.query(ancestor=key).fetch()
        dish_info = []
        if (len(dish_query)>0):
            for dish in dish_query:
                tmp = "/view_picture/%s" % dish.picture_key
                dish_info.append((dish.name, dish.price, tmp, dish.description))
        part =  urllib.urlencode({'name': restaurant_name})
        add_url = '/add_dish?%s' % part
        # self.response.write(restaurant_name)
        template = JINJA_ENVIRONMENT.get_template('templates/viewdishes.html')
        template_values ={
            'dish_query_len': len(dish_query),
            'dish_info': dish_info,
            'add_url': add_url,
            'restaurant_name': restaurant_name
        }
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/viewdishes.*', ViewDishHandler)
], debug=True)
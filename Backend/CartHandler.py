__author__ = 'rongshengxu'

from google.appengine.api import users
from google.appengine.ext import ndb
from handlers.DataModel import UserModel
import webapp2

import os
import jinja2
from handlers.DataModel import RestaurantModel, DishModel, OrderModel, CartModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CartHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        restaurant_name = self.request.get('restaurant_name')
        dish_name = self.request.get('dish_name')
        dish_price = float(self.request.get('dish_price'))
        quantity = int(self.request.get('quantity'))
        found = False
        restaurant = RestaurantModel.query(RestaurantModel.name==restaurant_name).fetch()[0]
        dish_query = DishModel.query(DishModel.name==dish_name, ancestor=restaurant.key).fetch()
        # self.response.write(dish_query[0].name)
        if (len(dish_query)>0):
            dish = dish_query[0]
            cart_query = CartModel.query(CartModel.user==user).fetch()
            if (len(cart_query)>0):
                cart = cart_query[0]
                name = []
                for order_key in cart.orders:
                    # order = OrderModel.get_by_id(order_key.id())
                    order = order_key.get()
                    dish_tmp = order.dish.get()
                    # name.append(order.dish.get().name)
                    if (dish_tmp.name==dish_name):
                        # self.response.write("get!!")
                        order.number = order.number + quantity
                        order.put()
                        cart.total = cart.total + dish_price*quantity
                        cart.put()
                        found = True
                        self.redirect("/order?name=%s" % restaurant.name)
                if (found == False):
                    new_order = OrderModel()
                    new_order.number = quantity
                    new_order.dish = dish.key
                    key = new_order.put()
                    cart.orders.append(key)
                    cart.total = cart.total + dish_price*quantity
                    cart.put()
                    self.redirect("/order?name=%s" % restaurant.name)
            else:
                self.redirect('/main')
        else:
            self.redirect('/main')

class ViewCartHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cart_query = CartModel.query(CartModel.user==user).fetch()
        cart_info = []
        if (len(cart_query)>0):
            cart = cart_query[0]
            for order_key in cart.orders:
                order = order_key.get()
                dish = order.dish.get()
                dish_name = dish.name
                dish_price = dish.price
                cart_info.append((dish_name, dish_price, order.number))
        template = JINJA_ENVIRONMENT.get_template('templates/viewcart.html')
        template_values = {
            'cart_query_len': len(cart_query),
            'cart_info': cart_info
        }
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/cart', CartHandler),
    ('/viewcart', ViewCartHandler)
], debug=True)
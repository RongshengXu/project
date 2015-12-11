__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

import os
import jinja2
import urllib
import json
from handlers.DataModel import RestaurantModel, DishModel, OrderModel, CartModel, HistoryCartModel

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
            cart_query = CartModel.query(CartModel.user==user, CartModel.restaurant_name==restaurant_name).fetch()
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
                new_order = OrderModel()
                new_order.number = quantity
                new_order.dish = dish.key
                key = new_order.put()
                cart = CartModel()
                cart.orders = []
                cart.orders.append(key)
                cart.total = quantity*dish.price
                cart.restaurant_name = restaurant_name
                cart.user = user
                cart.put()
                self.redirect("/order?name=%s" % restaurant.name)
                # self.redirect('/main')
        else:
            self.redirect('/main')

class ViewCartHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        carts_query = CartModel.query(CartModel.user==user).fetch()
        carts_info = []
        length = len(carts_query)
        if (len(carts_query)>0):
            for cart in carts_query:
                if (cart.total <= 0):
                    length = length - 1
                    cart.key.delete()
                    continue

                restaurant_name = cart.restaurant_name
                total = cart.total
                part = urllib.urlencode({'name': restaurant_name})
                cart_url = '/viewsinglecart?%s' % part
                # for order_key in cart.orders:
                #     order = order_key.get()
                #     dish = order.dish.get()
                #     dish_name = dish.name
                #     dish_price = dish.price
                carts_info.append((restaurant_name, total, cart_url))
        template = JINJA_ENVIRONMENT.get_template('templates/viewcart.html')
        template_values = {
            'cart_query_len': length,
            'cart_info': carts_info
        }
        self.response.write(template.render(template_values))

class ViewSingleCartHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        restaurant_name = self.request.get('name')
        restaurant = RestaurantModel.query(RestaurantModel.name==restaurant_name).fetch()[0]
        cart_query = CartModel.query(CartModel.restaurant_name==restaurant_name, CartModel.user==user).fetch()
        cart_info = []
        str = restaurant.payment
        # self.response.write(str)
        if (len(cart_query)>0):
            cart = cart_query[0]
            cart_total = cart.total
            if (len(cart.orders)>0):
                for order_key in cart.orders:
                    order = order_key.get()
                    dish = order.dish.get()
                    dish_name = dish.name
                    dish_price = dish.price
                    quantity = order.number
                    p = urllib.urlencode({'id':order_key.id(),'restaurant_name':restaurant_name})
                    cancel_url = "/cancel?%s" % p
                    cart_info.append((dish_name, dish_price, quantity, order_key.id(), cancel_url))
        part = urllib.urlencode({'restaurant_name': restaurant_name})
        confirm_url = '/confirm?%s' % part
        template = JINJA_ENVIRONMENT.get_template('templates/viewsinglecart.html')
        template_values = {
            'restaurant_name': restaurant_name,
            'cart_query_len': len(cart_query),
            'paypal': restaurant_name,
            'paypal_button': str,
            'cart_info': cart_info,
            'cart_total': cart_total,
            'confirm_url': confirm_url
        }
        self.response.write(template.render(template_values))

class ConfirmHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        restaurant_name = self.request.get('restaurant_name')
        # self.response.write(restaurant_name)
        restaurant = RestaurantModel.query(RestaurantModel.name == restaurant_name).fetch()[0]
        str = restaurant.payment
        cart = CartModel.query(CartModel.user==user, CartModel.restaurant_name==restaurant_name).fetch()[0]
        ######################################################Save the customer information (user address|phone|notes)###########################################################
        cart_id = cart.key.id()
        shipping_fee = restaurant.shipping_fee
        template = JINJA_ENVIRONMENT.get_template('templates/confirm.html')
        template_values = {
            'restaurant_name': restaurant_name,
            'total_cost': cart.total,
            'shipping_fee': shipping_fee,
            'payment': str,
            'cart_id': cart_id
        }
        self.response.write(template.render(template_values))

class PaymentHandler(webapp2.RequestHandler):
    def post(self):
        restaurant_name = self.request.get('restaurant_name')
        restaurant = RestaurantModel.query(RestaurantModel.name==restaurant_name).fetch()[0]
        payment = restaurant.payment
        info = {'payment': payment}
        info_json = json.dumps(info)
        self.response.write(info_json)
        # self.response.write("Test!!!!")

class PayHandler(webapp2.RequestHandler):
    def post(self):
        restaurant_name = self.request.get('restaurant_name')
        user = users.get_current_user()
        cart = CartModel.query(CartModel.user==user, CartModel.restaurant_name==restaurant_name).fetch()[0]
        ######################################################Send Email to restaurant###########################################################
        history_cart = HistoryCartModel()
        history_cart.restaurant_name = restaurant_name
        history_cart.user = user
        history_cart.total = cart.total
        history_cart.orders = cart.orders
        history_cart.put()
        cart.key.delete()
        self.response.write(json.dumps({'data': 'success'}))

app = webapp2.WSGIApplication([
    ('/cart', CartHandler),
    ('/viewcart', ViewCartHandler),
    ('/viewsinglecart', ViewSingleCartHandler),
    ('/confirm', ConfirmHandler),
    ('/payment', PaymentHandler),
    ('/paypal', PayHandler)
], debug=True)
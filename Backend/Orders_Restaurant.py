__author__ = 'Administrator'

from google.appengine.api import users
import webapp2

import os
import jinja2
from handlers.DataModel import HistoryCartModel
from handlers.DataModel import RestaurantModel
import urllib

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class OrdersToMeHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.write("My Orders")
        user = users.get_current_user()
        restaurant_list = RestaurantModel.query(RestaurantModel.owner==user).fetch()
        OrdersToMe_info = []
        for restaurant in restaurant_list:
            OrderToRestaurant_list = HistoryCartModel.query(HistoryCartModel.restaurant_name==restaurant.name).order(-HistoryCartModel.createTime).fetch()
            if (len(OrderToRestaurant_list)<=0):
                continue

            for OrderToRestaurant in OrderToRestaurant_list:
                time = OrderToRestaurant.createTime
                total = OrderToRestaurant.total
                order_info = []
                for order_key in OrderToRestaurant.orders:
                    order = order_key.get()
                    dish = order.dish.get()
                    order_info.append((dish.name, dish.price, order.number))
                OrdersToMe_info.append((("{:%a, %d %b %Y %H:%M:%S GMT}".format(time)), restaurant.name, OrderToRestaurant.user.nickname(), total, order_info))

        template = JINJA_ENVIRONMENT.get_template('templates/orders_restaurant.html')
        template_values = {
            'OrdersToMe_len': len(OrdersToMe_info),
            'OrdersToMe_info': OrdersToMe_info
        }
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/orders_restaurant', OrdersToMeHandler),
], debug=True)
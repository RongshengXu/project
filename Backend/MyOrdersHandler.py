__author__ = 'rongshengxu'

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

class MyOrdersHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.write("My Orders")
        user = users.get_current_user()
        history_cart_query = HistoryCartModel.query(HistoryCartModel.user==user).order(-HistoryCartModel.createTime).fetch()
        history_cart_info = []
        if (len(history_cart_query)>0):
            for history_cart in history_cart_query:
                restaurant_name = history_cart.restaurant_name
                time = history_cart.createTime
                total = history_cart.total
                order_info = []
                for order_key in history_cart.orders:
                    order = order_key.get()
                    dish = order.dish.get()
                    order_info.append((dish.name, dish.price, order.number))
                history_cart_info.append((("{:%a, %d %b %Y %H:%M:%S GMT}".format(time)), restaurant_name, total, order_info))

        template = JINJA_ENVIRONMENT.get_template('templates/myorders.html')
        template_values = {
            'history_cart_query_len': len(history_cart_query),
            'history_cart_info': history_cart_info
        }
        self.response.write(template.render(template_values))

class RateHandler(webapp2.RequestHandler):
    def get(self):
        URL = '/myorders'
        restaurant_name = self.request.get('restaurant_name')
        new_score = float(self.request.get('rate_score'))
        restaurant_list = RestaurantModel.query(RestaurantModel.name==restaurant_name).fetch()

        if (len(restaurant_list) > 0):
            restaurant = restaurant_list[0]
            if (restaurant.numberOfScores <= 0):
                restaurant.TotalScore = 0
            restaurant.TotalScore = round((restaurant.TotalScore * restaurant.numberOfScores + new_score)/(restaurant.numberOfScores + 1),2)
            restaurant.numberOfScores = restaurant.numberOfScores + 1
            restaurant.put()

        self.redirect(URL)

app = webapp2.WSGIApplication([
    ('/myorders', MyOrdersHandler),
    ('/rate', RateHandler)
], debug=True)
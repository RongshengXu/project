__author__ = 'rongshengxu'

from google.appengine.api import users
from handlers.DataModel import RestaurantModel, DishModel, UserModel
import webapp2

import os
import jinja2
import urllib
from handlers.DataModel import RestaurantModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class PlaceOrderHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        restaurant_name = self.request.get('name')
        restaurant = RestaurantModel.query(RestaurantModel.name==restaurant_name).fetch()[0]
        dish_query = DishModel.query(ancestor=restaurant.key).fetch()
        dish_info = []

        if (len(dish_query)>0):
            for dish in dish_query:
                pic_url = '/view_picture/%s' % dish.picture_key
                # p = urllib.urlencode({'restaurant_name':restaurant_name, 'dish_name': dish.name, 'dish_price': dish.price})
                # add_cart_url = "/cart?%s" % p
                dish_info.append((dish.name, dish.price, pic_url))
        template = JINJA_ENVIRONMENT.get_template('templates/order.html')
        part = urllib.urlencode({'name':restaurant_name})
        evaluate_url = "/evaluate?%s" % part
        template_values = {
            'evaluate_url': evaluate_url,
            'dish_query_len': len(dish_query),
            'restaurant_name': restaurant_name,
            'dish_info': dish_info
        }
        self.response.write(template.render(template_values))
        # self.response.write('Orders!!')

app = webapp2.WSGIApplication([
    ('/order.*', PlaceOrderHandler)
], debug=True)
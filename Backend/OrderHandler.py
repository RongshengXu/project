__author__ = 'rongshengxu'

from google.appengine.api import users
from handlers.DataModel import RestaurantModel, DishModel, UserModel
import webapp2

import os
import jinja2
from handlers.DataModel import RestaurantModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class PlaceOrderHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        restaurant_name = self.request.get('name')
        restaurant = RestaurantModel.query(RestaurantModel.name==restaurant_name, RestaurantModel.owner==user).fetch()[0]
        dish_query = DishModel.query(ancestor=restaurant.key).fetch()
        dish_info = []
        if (len(dish_query)>0):
            for dish in dish_query:
                pic_url = '/view_picture/%s' % dish.picture_key
                dish_info.append((dish.name, dish.price, pic_url))
        template = JINJA_ENVIRONMENT.get_template('templates/order.html')
        template_values = {
            'dish_query_len': len(dish_query),
            'restaurant_name': restaurant_name,
            'dish_info': dish_info
        }
        self.response.write(template.render(template_values))
        # self.response.write('Orders!!')

app = webapp2.WSGIApplication([
    ('/order.*', PlaceOrderHandler)
], debug=True)
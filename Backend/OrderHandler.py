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
        restaurant_img = "/view_picture/%s" % restaurant.Blob_key
        restaurant_score = restaurant.TotalScore
        restaurant_phone = restaurant.phoneNum
        restaurant_shippingfee = restaurant.shipping_fee
        restaurant_freeshipping = restaurant.free_shipping
        restaurant_location = restaurant.location

        dish_query = DishModel.query(ancestor=restaurant.key).fetch()
        dish_info = []

        if (len(dish_query)>0):
            for dish in dish_query:
                pic_url = '/view_picture/%s' % dish.picture_key
                # p = urllib.urlencode({'restaurant_name':restaurant_name, 'dish_name': dish.name, 'dish_price': dish.price})
                # add_cart_url = "/cart?%s" % p
                dish_info.append((dish.name, dish.price, pic_url, dish.description))
        template = JINJA_ENVIRONMENT.get_template('templates/order.html')
        part = urllib.urlencode({'name':restaurant_name})
        evaluate_url = "/evaluate?%s" % part
        template_values = {
            'evaluate_url': evaluate_url,
            'dish_query_len': len(dish_query),
            'restaurant_name': restaurant_name,
            'restaurant_img': restaurant_img,
            'restaurant_score': restaurant_score,
            'restaurant_phone': restaurant_phone,
            'restaurant_shippingfee': restaurant_shippingfee,
            'restaurant_freeshipping': restaurant_freeshipping,
            'restaurant_location': restaurant_location,
            'dish_info': dish_info
        }
        self.response.write(template.render(template_values))
        # self.response.write('Orders!!')

app = webapp2.WSGIApplication([
    ('/order.*', PlaceOrderHandler)
], debug=True)
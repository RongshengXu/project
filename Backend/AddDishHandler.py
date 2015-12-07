__author__ = 'rongshengxu'

from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import ndb

import webapp2
import urllib

from handlers.DataModel import RestaurantModel, DishModel

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class DishRegisterPage(webapp2.RequestHandler):
    def get(self):
        restaurant_name = self.request.get('name')
        upload_url = blobstore.create_upload_url('/dish_handler')
        template_values = {
            'upload_url': upload_url,
            'restaurant_name': restaurant_name
        }
        template = JINJA_ENVIRONMENT.get_template("templates/adddish.html")
        self.response.write(template.render(template_values))

class DishRegister(blobstore_handlers.BlobstoreUploadHandler):
    """
        upload cover picture and other information for a restaurant
    """
    def post(self):
        user = users.get_current_user()
        upload = self.get_uploads()[0]
        restaurant_name = self.request.get('restaurant_name')
        restaurant_query = RestaurantModel.query(RestaurantModel.name==restaurant_name, RestaurantModel.owner==user).fetch()
        if (len(restaurant_query)>0) :
            # u = "%s" % user
            # self.response.write(restaurant_name +" " +  u)
            restaurant = restaurant_query[0]
            dish = DishModel(parent=restaurant.key)
            dish.name = self.request.get('dish_name')
            dish.price = float(self.request.get('dish_price'))
            dish.picture_key = upload.key()
            dish.put()
            self.redirect('/main_restaurant')
        else:
            self.redirect('/error')

app = webapp2.WSGIApplication([
    ('/add_dish.*', DishRegisterPage),
    ('/dish_handler', DishRegister)
], debug=True)

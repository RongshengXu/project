__author__ = 'rongshengxu'

from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import ndb

import webapp2
import urllib

from handlers.DataModel import RestaurantModel

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class RegisterPage(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/register')
        template_values = {
            'upload_url': upload_url
        }
        template = JINJA_ENVIRONMENT.get_template("templates/restaurantregister.html")
        self.response.write(template.render(template_values))
        # self.response.write("Register!!!")

class Register(blobstore_handlers.BlobstoreUploadHandler):
    """
        upload cover picture and other information for a restaurant
    """
    def post(self):
        restaurant = RestaurantModel()
        restaurant.name = self.request.get('name')
        restaurant.owner = users.get_current_user()
        restaurant.ownerName = self.request.get('ownername')
        restaurant.phoneNum = self.request.get('phonenumber')
        restaurant.location = self.request.get('location')
        if (self.request.get('latitude')!=""):
            restaurant.latitude = float(self.request.get('latitude'))
        if (self.request.get('longitude')!=""):
            restaurant.longitude = float(self.request.get('longitude'))
        upload_query = self.get_uploads()
        if len(upload_query)>0:
            upload = self.get_uploads()[0]
            restaurant.Blob_key = upload.key()
        restaurant.comments = []
        restaurant.numberOfScores = 0
        if (self.request.get('freeshipping')!=""):
            restaurant.free_shipping = float(self.request.get('freeshipping'))
        if (self.request.get('shipping')!=""):
            restaurant.shipping_fee = float(self.request.get('shipping'))
        restaurant.payment = self.request.get('paypal')
        restaurant.put()
        # self.redirect('/view_picture/%s' % restaurant.Blob_key)
        # img = self.request.get('img')
        # img = images.resize(img, 64,64)
        # restaurant.coverPage = img
        self.redirect('/main_restaurant')

class ViewPictureHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)

class ViewEditHandler(webapp2.RequestHandler):
    def get(self):
        restaurant_name = self.request.get('restaurant_name')
        user = users.get_current_user()
        restaurant_query = RestaurantModel.query(RestaurantModel.owner==user, RestaurantModel.name==restaurant_name).fetch()
        restaurant_info = []
        if (len(restaurant_query)>0):
            restaurant = restaurant_query[0]
            viewURL = '/view_picture/%s' % restaurant.Blob_key
            restaurant_info.append((restaurant_name, restaurant.ownerName, restaurant.location, restaurant.free_shipping,
                                restaurant.shipping_fee, viewURL))
        template = JINJA_ENVIRONMENT.get_template('viewedit.html')
        template_values = {

        }
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/restaurantregister', RegisterPage),
    ('/register', Register)
], debug=True)

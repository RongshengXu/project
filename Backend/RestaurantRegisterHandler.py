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
        upload = self.get_uploads()[0]
        restaurant = RestaurantModel()
        restaurant.name = self.request.get('name')
        restaurant.owner = users.get_current_user()
        restaurant.ownerName = self.request.get('ownername')
        restaurant.phoneNum = self.request.get('phonenumber')
        restaurant.location = self.request.get('location')
        restaurant.latitude = float(self.request.get('latitude'))
        restaurant.longitude = float(self.request.get('longitude'))
        restaurant.Blob_key = upload.key()
        restaurant.comments = []
        restaurant.numberOfScores = 0
        restaurant.free_shipping = float(self.request.get('freeshipping'))
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

app = webapp2.WSGIApplication([
    ('/restaurantregister', RegisterPage),
    ('/register', Register)
], debug=True)

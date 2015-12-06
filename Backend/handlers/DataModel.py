__author__ = 'rongshengxu'

from google.appengine.ext import ndb
from google.appengine.ext import db

class RestaurantModel(ndb.Model):
    """ restaurant model
    """
    name = ndb.StringProperty()
    owner = ndb.UserProperty()
    ownerName = ndb.StringProperty()
    location = ndb.StringProperty()
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    coverPage = ndb.BlobProperty()
    Blob_key = ndb.BlobKeyProperty()
    createTime = ndb.DateTimeProperty(auto_now_add=True)
    payment = ndb.StringProperty()
    type = ndb.StringProperty(repeated=True)

class CartModel(ndb.Model):
    """ cart to store current orders
    """
    orders = ndb.KeyProperty(kind='OrderModel', repeated=True)

class DishModel(ndb.Model):
    """ dish model
    """
    name = ndb.StringProperty()
    price = ndb.FloatProperty()
    picture_key = ndb.BlobKeyProperty()

class UserModel(ndb.Model):
    """ User model
        store order and location history
    """
    user = ndb.UserProperty()
    lastLocation = ndb.StringProperty()
    orders = ndb.KeyProperty(kind='OrderModel', repeated=True)

class OrderModel(ndb.Model):
    """
        order model
    """
    dish = ndb.KeyProperty(kind='DishModel')
    number = ndb.IntegerProperty()
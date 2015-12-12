__author__ = 'rongshengxu'

from google.appengine.ext import ndb

class RestaurantModel(ndb.Model):
    """ restaurant model
    """
    name = ndb.StringProperty()
    owner = ndb.UserProperty()
    ownerName = ndb.StringProperty()
    phoneNum = ndb.StringProperty()
    location = ndb.StringProperty()
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    # coverPage = ndb.BlobProperty()
    Blob_key = ndb.BlobKeyProperty()

    TotalScore = ndb.FloatProperty()
    numberOfScores = ndb.IntegerProperty()
    free_shipping = ndb.FloatProperty()
    shipping_fee = ndb.FloatProperty()

    createTime = ndb.DateTimeProperty(auto_now_add=True)
    payment = ndb.StringProperty(indexed=False)
    type = ndb.StringProperty(repeated=True)

class CartModel(ndb.Model):
    """ cart to store current orders
    """
    user = ndb.UserProperty()
    restaurant_name = ndb.StringProperty()
    orders = ndb.KeyProperty(kind='OrderModel', repeated=True)
    total = ndb.FloatProperty()

    customer_address = ndb.StringProperty()
    customer_phone = ndb.StringProperty()
    customer_time = ndb.StringProperty()
    customer_notes = ndb.StringProperty()

class HistoryCartModel(ndb.Model):
    """      store user cart history
    """
    user = ndb.UserProperty()
    restaurant_name = ndb.StringProperty()
    orders = ndb.KeyProperty(kind='OrderModel', repeated=True)
    total = ndb.FloatProperty()
    createTime = ndb.DateTimeProperty(auto_now_add=True)

class DishModel(ndb.Model):
    """ dish model
    """
    name = ndb.StringProperty()
    price = ndb.FloatProperty()
    description = ndb.StringProperty()
    picture_key = ndb.BlobKeyProperty()
    # restaurant_key = ndb.KeyProperty(kind=RestaurantModel)

class UserModel(ndb.Model):
    """ User model
        store order and location history
    """
    user = ndb.UserProperty()
    last_location = ndb.StringProperty()
    last_latitude = ndb.FloatProperty()
    last_longitude = ndb.FloatProperty()
    orders = ndb.KeyProperty(kind='HistoryCartModel', repeated=True)

class OrderModel(ndb.Model):
    """     order model
    """
    restaurant_name = ndb.StringProperty()
    dish = ndb.KeyProperty(kind='DishModel')
    number = ndb.IntegerProperty()

class CommentModel(ndb.Model):
    """     comment model
    """
    user = ndb.UserProperty()
    restaurant_name = ndb.StringProperty()
    createTime = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.StringProperty()


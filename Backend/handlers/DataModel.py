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

    # lastUpdated = ndb.DateTimeProperty(auto_now=True)
    # url = ndb.StringProperty()
    # tag = ndb.StringProperty(repeated=True)
    # subscribers = ndb.StringProperty(repeated=True)
    # message = ndb.StringProperty()
    # coverpageURL = ndb.StringProperty()
    # totalPicture = ndb.IntegerProperty()

class DishModel(ndb.Model):
    """ picture model
    """
    name = ndb.StringProperty()
    price = ndb
    picture = db.BlobProperty()
    # lat = db.FloatProperty()
    # lg = db.FloatProperty()
    # #stream = db.StringProperty()
    # id = db.StringProperty()
    # uploadDate = db.DateTimeProperty(auto_now_add=True)
    # Date = db.DateProperty(auto_now_add=True)


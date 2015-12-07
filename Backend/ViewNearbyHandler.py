__author__ = 'rongshengxu'

import webapp2
import os
import jinja2
from handlers.DataModel import RestaurantModel, DishModel, UserModel
from google.appengine.ext import ndb
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ViewNearbyPage(webapp2.RequestHandler):
    def post(self):
        u = users.get_current_user()
        name = self.request.get('location')
        dis = self.request.get('distance')
        lat = float(self.request.get('latitude'))
        lg = float(self.request.get('longitude'))
        user_query = UserModel.query(UserModel.user==u).fetch()
        if (len(user_query)>0):
            user = user_query[0]
        else:
            user = UserModel()
            user.user = u
        user.last_latitude = lat
        user.last_longitude = lg
        user.last_location = name
        user.put()
        self.redirect('/main')
        # restaurant_query = RestaurantModel.query().fetch()
        # restaurant_info = []
        # info = []
        # if (len(restaurant_query)>0):
        #     for restaurant in restaurant_query:
        #         l = restaurant.latitude
        #         a = restaurant.longitude
        #         restaurant_info.append((restaurant.name, a, l))
        # restaurant_info.sort(key=lambda tup: (tup[2]-lat)**2 + (tup[1]-lg)**2)
        # template = JINJA_ENVIRONMENT.get_template('templates/viewnearby.html')
        # template_values = {
        #     "location": name,
        #     "distance": dis,
        #     "restaurant_info": restaurant_info
        # }
        # self.response.write(template.render(template_values))
        # self.response.write(restaurant_info)

app = webapp2.WSGIApplication([
    ('/viewnearby', ViewNearbyPage)
], debug=True)
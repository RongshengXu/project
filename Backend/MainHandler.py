__author__ = 'rongshengxu'

from google.appengine.api import users
from handlers.DataModel import UserModel
import webapp2

import os
import jinja2
from handlers.DataModel import RestaurantModel, CartModel
import urllib

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

sort_dist = True

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        global sort_dist

        if (user):
            u_query = UserModel.query(UserModel.user==user).fetch()
            if (len(u_query)>0):
                u = u_query[0]
                current_location = u.last_location
                lat = u.last_latitude
                lg = u.last_longitude
                url = users.create_logout_url(self.request.url)
                url_linktext = 'Logout'
                restaurant_query = RestaurantModel.query().order(-RestaurantModel.TotalScore).fetch()
                restaurant_info = []
                if (len(restaurant_query) > 0):
                    for restaurant in restaurant_query:
                        a = restaurant.latitude
                        l = restaurant.longitude
                        tmp = "/view_picture/%s" % restaurant.Blob_key
                        part = urllib.urlencode({'name':restaurant.name})
                        tmp1 = "/order?%s" % part
                        score = restaurant.TotalScore
                        restaurant_info.append((restaurant.name, tmp, a, l, tmp1, score))

                if (sort_dist):
                    restaurant_info.sort(key=lambda tup: (tup[2]-lat)**2+(tup[3]-lg)**2)

                # # Initialize a cart for this user
                # cart_query = CartModel.query(CartModel.user==user).fetch()
                # if (len(cart_query)<1):
                #     cart = CartModel()
                #     cart.user = user
                #     cart.orders = []
                #     cart.total = 0.0
                #     cart.put()

                # current_location = 'UT-Austin'              #get the current location in database
                template_values = {
                    'user': user,
                    'url': url,
                    'url_linktext': url_linktext,
                    'current_location': current_location,
                    'restaurant_query_len': len(restaurant_query),
                    'restaurant_info': restaurant_info
                }
                template = JINJA_ENVIRONMENT.get_template('templates/main.html')
                self.response.write(template.render(template_values))
            else:
                self.redirect('/location')
        else:
            self.redirect('/')

class ChangeToDistance(webapp2.RequestHandler):
    def get(self):
        global sort_dist
        sort_dist = True
        self.redirect('/main')

class ChangeToValuation(webapp2.RequestHandler):
    def get(self):
        global sort_dist
        sort_dist = False
        self.redirect('/main')

app = webapp2.WSGIApplication([
    ('/main', MainPage),
    ('/change_sort_to_distance', ChangeToDistance),
    ('/change_sort_to_valuation', ChangeToValuation),
], debug=True)
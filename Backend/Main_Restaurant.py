from google.appengine.api import users

import webapp2

import os
import jinja2
from handlers.DataModel import RestaurantModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if (user):

            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
            restaurant_query = RestaurantModel.query(RestaurantModel.owner==user).fetch()
            restaurant_info = []
            if (len(restaurant_query) > 0):
                for restaurant in restaurant_query:
                    tmp = "/view_picture/%s" % restaurant.Blob_key
                    restaurant_info.append((restaurant.name, tmp))
            current_location = 'UT-Austin'              #get the current location in database

            template_values = {
                'user': user,
                'url': url,
                'url_linktext': url_linktext,
                'current_location': current_location,
                'restaurant_query_len': len(restaurant_query),
                'restaurant_info': restaurant_info
            }
            template = JINJA_ENVIRONMENT.get_template('templates/main_restaurant.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/main_restaurant', MainPage)
], debug=True)

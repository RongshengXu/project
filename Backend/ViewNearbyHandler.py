__author__ = 'rongshengxu'

import webapp2
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ViewNearbyPage(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('location')
        dis = self.request.get('distance')
        lat = self.request.get('latitude')
        lg = self.request.get('longitude')
        template = JINJA_ENVIRONMENT.get_template('templates/viewnearby.html')
        template_values = {
            "location": name,
            "distance": dis,
        }
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/viewnearby', ViewNearbyPage)
], debug=True)
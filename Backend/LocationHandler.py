__author__ = 'rongshengxu'

from google.appengine.api import users

import webapp2
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class LocationPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.url)
        url_linktext = 'Logout'

        template_values = {
                'user': user,
                'url': url,
                'url_linktext': url_linktext,
            }

        template = JINJA_ENVIRONMENT.get_template('templates/location.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/location', LocationPage)
], debug=True)


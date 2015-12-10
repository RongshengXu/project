from google.appengine.api import users

from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.ext import blobstore

import webapp2

import sys
import os
import jinja2
import json
import datetime
from handlers.DataModel import RestaurantModel
from handlers.DataModel import CommentModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

restaurant_name = ''

class EvaluatePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        global restaurant_name
        restaurant_name = self.request.get('name')
        restaurant = RestaurantModel.query(RestaurantModel.name==restaurant_name).fetch()[0]
        restaurant_img = "/view_picture/%s" % restaurant.Blob_key
        restaurant_score = restaurant.TotalScore
        restaurant_phone = restaurant.phoneNum
        restaurant_shippingfee = restaurant.shipping_fee
        restaurant_freeshipping = restaurant.free_shipping

        if (user):
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
            order_url = "/order?name=%s" % restaurant_name

            # Get all the comments to the restaurant
            comments_list = []
            comments_query = CommentModel.query(CommentModel.restaurant_name==restaurant_name).order(-CommentModel.createTime).fetch()
            comment_time = datetime.datetime.now()

            if (len(comments_query)>0):
                for comment in comments_query:
                    comment_time = "{:%a, %d %b %Y %H:%M:%S GMT}".format(comment.createTime)

                    comments_list.append((comment_time, comment.user.nickname(), comment.content))

            num_of_comments = len(comments_list)
            template_values = {
                'order_url': order_url,
                'restaurant_name': restaurant_name,
                'restaurant_img': restaurant_img,
                'restaurant_score': restaurant_score,
                'restaurant_phone': restaurant_phone,
                'restaurant_shippingfee': restaurant_shippingfee,
                'restaurant_freeshipping': restaurant_freeshipping,
                'user': user,
                'url': url,
                'url_linktext': url_linktext,
                'num_of_comments': num_of_comments,
                'comments_list': comments_list,
            }
            template = JINJA_ENVIRONMENT.get_template('templates/evaluate.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

class UserInfo(webapp2.RequestHandler):
    def get(self):
        comment_content = self.request.get('comment')

        comment = CommentModel()
        comment.restaurant_name = restaurant_name
        comment.user = users.get_current_user()
        comment.content = comment_content
        comment.put()

        userLogo = "http://www.gnosko.com/dist/img/unknown.gif"
        #userInfo = {"name": comment, "logo": userLogo}
        userInfo = {"name": users.get_current_user().nickname(), "logo": userLogo}

        # self.response.headers['Content-Type'] = 'application/json'
        userInfo_json = json.dumps(userInfo)
        self.response.write(userInfo_json)

app = webapp2.WSGIApplication([
    ('/evaluate', EvaluatePage),
    ('/getuserinfo', UserInfo)
], debug=True)

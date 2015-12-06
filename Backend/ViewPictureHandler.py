__author__ = 'rongshengxu'
import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

class ViewPictureHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            # self.response.headers['Content-Type'] = 'image/png'
            self.send_blob(photo_key)

app = webapp2.WSGIApplication([
    ('/view_picture/([^/]+)?', ViewPictureHandler)
], debug=True)

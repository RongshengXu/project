__author__ = 'rongshengxu'
import webapp2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

class PictureUploadFormHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload_picture')
        # The method must be "POST" and enctype must be set to "multipart/form-data".
        self.response.write('<html><body>')
        self.response.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.write('''Upload File: <input type="file" name="file"><br> <input type="submit"
            name="submit" value="Submit"> </form></body></html>''')

class PictureUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            user_photo = UserPhoto(user=users.get_current_user().user_id(),
                                   blob_key=upload.key())
            user_photo.put()

            self.redirect('/view_photo/%s' % upload.key())
        except:
            self.redirect('/upload_failure.html')

app = webapp2.WSGIApplication([('/upload_form', PhotoUploadFormHandler),
                                ('/upload_picture', PictureUploadHandler)
                              ], debug=True)

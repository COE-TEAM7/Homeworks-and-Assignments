import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json
from google.appengine.api import users
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
##########################NEW THESIS ENTRY#######################################

class thesisEntry(ndb.Model):
    Title = ndb.StringProperty(indexed = True)
    Adviser = ndb.StringProperty(indexed = True)
    Abstract = ndb.StringProperty(indexed = True)
    Year = ndb.IntegerProperty(indexed = True)
    Section = ndb.IntegerProperty(indexed = True)
    Date = ndb.DateTimeProperty(auto_now_add = True)

# class MyHandler(webapp2.RequestHandler):
#     def get(self):
         
#         user = users.get_current_user()
#         myPage = """
#           <html>
#             <body>
#                 <div>
#                     <h2>Google App Engine Login - Python Web app</h2>
#                     <h3>Welcome, {0}. This is a sample page!</h3>
#                     <a href="{1}"><b>Click here to {2}</b></a>
#                 </div>
#             </body>
#           </html>
#           """
#         if user:
#             myData = myPage.format(user.nickname(), users.create_logout_url("/"),'logout' )
#         else:
#             myData = myPage.format('Guest', users.create_login_url("/"),'login' )
             
#         self.response.out.write(myData)
         
# class SecuredPage(webapp2.RequestHandler):
#     def get(self):
#         myPage = """
#           <html>
#             <body>
#                 <div>
#                     <h2>Google App Engine Login - Python Web app</h2>
#                     <h3>Welcome, {0}. This page is secured! Nice that you could login.</h3>
#                     <a href="{1}"><b>Click here to {2}</b></a>
#                 </div>
#             </body>
#           </html>
#           """
         
#         user = users.get_current_user()
#         myData = myPage.format(user.nickname(), users.create_logout_url("/"),'logout' )
#         self.response.out.write(myData)

class loginPage(webapp2.RequestHandler):
    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render())
            greeting = ('Welcome, %s! (<a href="%s">Sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            greeting = ('Please <a href="%s">Log in</a> if you want to add an entry to the list.' %
                        users.create_login_url('/'))

        self.response.out.write('<div class="login">%s</div>' % greeting)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render())

    def post(self):
    	thesis = thesisEntry()
    	thesis.Title = self.request.get('thesis_title')
    	thesis.Adviser = self.request.get('thesis_adviser')
    	thesis.Abstract = self.request.get('thesis_abstract')
    	thesis.Year = int(self.request.get('thesis_year'))
    	thesis.Section = int(self.request.get('thesis_section'))
    	thesis.put()

class APIThesisDeleteHandler(webapp2.RequestHandler):
    def get(self, thesis_id):
        thesis_key = ndb.Key(urlsafe=thesis_id)
        thesis = thesis_key.get()
        thesis.key.delete()
        time.sleep(0.1)
        self.redirect('/')

class apiThesis(webapp2.RequestHandler):
    def post(self):
    	thesis = thesisEntry()
    	thesis.Title = self.request.get('thesis_title')
    	thesis.Adviser = self.request.get('thesis_adviser')
    	thesis.Abstract = self.request.get('thesis_abstract')
    	thesis.Year = int(self.request.get('thesis_year'))
    	thesis.Section = int(self.request.get('thesis_section'))
    	thesis.put()
        self.response.headers['Content-Type'] = 'app/json'
        response = {
            'result': 'OK',
            'data': {
                'id':thesis.key.urlsafe(),
                'thesis_title': thesis.Title,
                'thesis_year': thesis.Year,
                'thesis_abstract': thesis.Abstract,
                'thesis_adviser': thesis.Adviser,
                'thesis_section': thesis.Section
            }
        }
        self.response.out.write(json.dumps(response))

    def get(self):
        thesis = thesisEntry.query().order(-thesisEntry.Date).fetch()
        thesis_list = []
        for t in thesis:
            thesis_list.append({
                'id':t.key.urlsafe(),
                'thesis_title': t.Title,
                'thesis_year': t.Year,
                'thesis_abstract': t.Abstract,
                'thesis_adviser': t.Adviser,
                'thesis_section': t.Section
                })
        response = {
            'results': 'OK',
            'data': thesis_list
        }
        self.response.headers['Content-Type'] = 'app/json'
        self.response.out.write(json.dumps(response))


app = webapp2.WSGIApplication([
	('/', loginPage),
    ('/home', MainPageHandler),
    ('/api/thesis', apiThesis),
    ('/api/thesis/delete/(.*)', APIThesisDeleteHandler)
], debug=True)
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

class User(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    first_name = ndb.StringProperty(indexed = True)
    last_name = ndb.StringProperty(indexed = True)
    phone_number = ndb.IntegerProperty(indexed = True)
    created_date = ndb.DateTimeProperty(auto_now_add = True)

# class createUser(webapp2.RequestHandler):
#     def get(self):
#         user1 = User(email='wil@gmail.com', first_name = 'Wil', last_name = 'Villanueva')
#         user1.put()
#         logging.info(user1)

#         user2 = User(id = '123456', email='wil@gmail.com', first_name = 'Will', last_name = 'Villanueva')
#         user2.put()
#         logging.info(user2)

#         user3 = User(id = '123456', email='wwwil@gmail.com', first_name = 'Wwill', last_name = 'vVillanueva')
#         user3.put()
#         logging.info(user3)

# class testPage(webapp2.RequestHandler):
#     def get(self):
#         user_key = ndb.Key('User', '123456')
#         user2 = user_key.get()
#         #to edit
#         user3_key = ndb.Key('User', '123456')
#         user3 = user3_key.get()
#         user3.last_name = 'GGGGG'
#         user3.put()
#         #checking logs
#         logging.info(user2)
#         logging.info(user_key)
#         logging.info(user_key.id())
#         logging.info(user_key.urlsafe())
#         logging.info(user_key.get())

class registerPageHandler(webapp2.RequestHandler):
    def get(self):
        loggedin_user = users.get_current_user()
        if loggedin_user:
            user_key= ndb.Key('User', loggedin_user.user_id())
            user = user_key.get()
            if user:
                self.redirect('/home')
                # logout_url = users.create_logout_url('/')
                # template_values = {
                #     'logout_url': logout_url,
                #     'loggedin_user': loggedin_user,
                # }
                # template = JINJA_ENVIRONMENT.get_template('main.html')
                # self.response.write(template.render(template_values))
            else:
                self.response.write('You need to register first')
                logout_url = users.create_logout_url('/home')
                template_values = {
                    'logout_url': logout_url,
                    'loggedin_user': loggedin_user,
                }
                template = JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render(template_values))
            # login_url = users.create_login_url('/home')
            # logout_url = users.create_logout_url('/')
            # template_values = {
            #     'login_url': login_url,
            #     'logout_url': logout_url,
            #     'loggedin_user': loggedin_user,
            # }
            # template = JINJA_ENVIRONMENT.get_template('main.html')
            # self.response.write(template.render(template_values))
        else:
            self.redirect('/login')

    def post(self):
        loggedin_user = users.get_current_user()
        user = User(id = loggedin_user.user_id(), email = loggedin_user.email())
        user.first_name = self.request.get('first_name')
        user.last_name = self.request.get('last_name')
        user.phone_number = int(self.request.get('phone_number'))
        user.put()
        self.redirect('/')

class thesisEntry(ndb.Model):
    Title = ndb.StringProperty(indexed = True)
    Adviser = ndb.StringProperty(indexed = True)
    Created_by = ndb.StringProperty(indexed = True)
    Abstract = ndb.StringProperty(indexed = True)
    Year = ndb.IntegerProperty(indexed = True)
    Section = ndb.IntegerProperty(indexed = True)
    Date = ndb.DateTimeProperty(auto_now_add = True)

class loginPage(webapp2.RequestHandler):
    def get(self):
        # Checks for active Google account session
        loggedin_user = users.get_current_user()
        if loggedin_user:
            user_key= ndb.Key('User', loggedin_user.user_id())
            user = user_key.get()
            if user:
                self.redirect('/home')
                # logout_url = users.create_logout_url('/')
                # template_values = {
                #     'logout_url': logout_url,
                #     'loggedin_user': loggedin_user,
                # }
                # template = JINJA_ENVIRONMENT.get_template('main.html')
                # self.response.write(template.render(template_values))
            else:
                self.response.write('You need to register first')
                logout_url = users.create_logout_url('/home')
                template_values = {
                    'logout_url': logout_url,
                    'loggedin_user': loggedin_user,
                }
                template = JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render(template_values))
            # login_url = users.create_login_url('/home')
            # logout_url = users.create_logout_url('/')
            # template_values = {
            #     'login_url': login_url,
            #     'logout_url': logout_url,
            #     'loggedin_user': loggedin_user,
            # }
            # template = JINJA_ENVIRONMENT.get_template('main.html')
            # self.response.write(template.render(template_values))
        else:
            login_url = users.create_login_url('/home')
            template_values = {
                'login_url': login_url,
            }
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))

class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        loggedin_user = users.get_current_user()
        if loggedin_user:
            user_key= ndb.Key('User', loggedin_user.user_id())
            user = user_key.get()
            if user:
                logout_url = users.create_logout_url('/home')
                template_values = {
                    'logout_url': logout_url,
                    'loggedin_user': loggedin_user,
                }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))
            else:
                self.response.write('You need to register first')
                login_url = users.create_login_url('/register')
                logout_url = users.create_logout_url('/home')
                template_values = {
                    'login_url': login_url,
                    'logout_url': logout_url,
                    'loggedin_user': loggedin_user,
                }
                template = JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render(template_values))
            # login_url = users.create_login_url('/home')
            # logout_url = users.create_logout_url('/')
            # template_values = {
            #     'login_url': login_url,
            #     'logout_url': logout_url,
            #     'loggedin_user': loggedin_user,
            # }
            # template = JINJA_ENVIRONMENT.get_template('main.html')
            # self.response.write(template.render(template_values))
        else:
            self.redirect('/login')
            # login_url = users.create_login_url('/')
            # template_values = {
            #     'login_url': login_url,
            # }
            # template = JINJA_ENVIRONMENT.get_template('index.html')
            # self.response.write(template.render(template_values))

    def post(self):
    	thesis = thesisEntry()
        user = users.get_current_user()
    	thesis.Title = self.request.get('thesis_title')
    	thesis.Adviser = self.request.get('thesis_adviser')
    	thesis.Abstract = self.request.get('thesis_abstract')
    	thesis.Year = int(self.request.get('thesis_year'))
    	thesis.Section = int(self.request.get('thesis_section'))
        thesis.Created_by = user.nickname()
    	thesis.put()
        self.redirect('/')

class APIThesisDeleteHandler(webapp2.RequestHandler):
    def get(self, thesis_id):
        thesis_key = ndb.Key(urlsafe=thesis_id)
        thesis = thesis_key.get()
        thesis.key.delete()
        time.sleep(0.1)
        self.redirect('/')

class editThesis(webapp2.RequestHandler):
    def post(self):
        thesis_key = ndb.Key(urlsafe = thesis_id)
        thesis = thesis_key.get()
        user = users.get_current_user()
        thesis = thesisEntry()
        thesis.Title = self.request.get('thesis_title')
        thesis.Adviser = self.request.get('thesis_adviser')
        thesis.Abstract = self.request.get('thesis_abstract')
        thesis.Year = int(self.request.get('thesis_year'))
        thesis.Section = int(self.request.get('thesis_section'))
        thesis.Created_by = user.nickname()
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
        self.redirect('/login')

class apiThesis(webapp2.RequestHandler):
    def post(self):
        thesis_key = ndb.Key(urlsafe = thesis_id)
        thesis = thesis_key.get()
        user = users.get_current_user()
    	thesis = thesisEntry()
    	thesis.Title = self.request.get('thesis_title')
    	thesis.Adviser = self.request.get('thesis_adviser')
    	thesis.Abstract = self.request.get('thesis_abstract')
    	thesis.Year = int(self.request.get('thesis_year'))
    	thesis.Section = int(self.request.get('thesis_section'))
        thesis.Created_by = user.nickname()
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
        self.redirect('/login')

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
                'thesis_section': t.Section,
                'thesis_author':t.Created_by
                })
        response = {
            'results': 'OK',
            'data': thesis_list
        }
        self.response.headers['Content-Type'] = 'app/json'
        self.response.out.write(json.dumps(response))

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/home')

app = webapp2.WSGIApplication([
	('/login', loginPage),
    ('/', MainPageHandler),
    ('/home', HomePageHandler),
    ('/api/thesis', apiThesis),
    ('/api/thesis/delete/(.*)', APIThesisDeleteHandler),
    ('/api/thesis/edit/(.*)', editThesis),
    ('/register', registerPageHandler)
], debug=True)
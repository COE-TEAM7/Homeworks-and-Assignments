import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json


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
        thesiss = thesisEntry.query().order(-thesisEntry.Date).fetch()
        thesis_list = []
        for thesis in thesiss:
            thesis_list.append({
                'id':thesis.key.urlsafe(),
                'thesis_title': thesis.Title,
                'thesis_year': thesis.Year,
                'thesis_abstract': thesis.Abstract,
                'thesis_adviser': thesis.Adviser,
                'thesis_section': thesis.Section
                })
        response = {
            'results': 'OK',
            'data': thesis_list
        }
        self.response.headers['Content-Type'] = 'app/json'
        self.response.out.write(json.dumps(response))


app = webapp2.WSGIApplication([
	('/', MainPageHandler),
    ('/home', MainPageHandler),
    ('/api/thesis', apiThesis)
], debug=True)
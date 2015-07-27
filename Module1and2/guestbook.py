import os
import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import logging
from google.appengine.ext.webapp import template

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign?%s" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    <hr>
    <form>Guestbook name:
      <input value="%s" name="guestbook_name">
      <input type="submit" value="switch">
    </form>
    <a href="%s">%s</a>
  </body>
</html>
"""

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class GuestbookPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        
class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

##################### CRUD ####################################
class Student(ndb.Model):
    First_name = ndb.StringProperty(indexed = True)
    Last_name = ndb.StringProperty(indexed = True)
    Age = ndb.IntegerProperty(indexed = True)
    Date = ndb.DateTimeProperty(auto_now_add = True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!!''<br />')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(' <a href="/guestbook">Module 1 - Guestbook</a>')
        self.response.write('<br />'' <a href="/student/create">Module 2 - CRUD</a>')

class SuccessCreate(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('success-create.html')
        self.response.write(template.render())

class SuccessEdit(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('success-edit.html')
        self.response.write(template.render())

class SuccessDelete(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('success-delete.html')
        self.response.write(template.render())

class StudentCreatePage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('create_student.html')
        self.response.write(template.render())

    def post(self):
        student = Student()
        student.First_name = self.request.get('first_name')
        student.Last_name = self.request.get('last_name')
        student.Age = int(self.request.get('age'))
        student.put()
        self.redirect('/success-create')

class StudentList(webapp2.RequestHandler):
    def get(self):
        students = Student.query().order(-Student.Date).fetch()
        logging.info(students)
        template_data = {
            'student_list': students
            }
        template = JINJA_ENVIRONMENT.get_template('student_list.html')
        self.response.write(template.render(template_data))

class ProfilePage(webapp2.RequestHandler):
    def get(self,student_id):
        students=Student.get_by_id(int(student_id))
        template_data={
            'student_list':students
        }
        template=JINJA_ENVIRONMENT.get_template('student-profile.html')
        self.response.write(template.render(template_data))

class DeletePage(webapp2.RequestHandler):
    def get(self,studID):
        students = Student.get_by_id(int(studID))
        students.key.delete()
        self.redirect('/success-delete')

class EditPage(webapp2.RequestHandler):
    def get(self,studID):
        students = Student.get_by_id(int(studID))
        template_data = {
            'student_list': students
            }
        template = JINJA_ENVIRONMENT.get_template('editpage.html')
        self.response.write(template.render(template_data))

    def post(self,studID):
        students = Student.get_by_id(int(studID))
        students.First_name = self.request.get('first_edit')
        students.Last_name = self.request.get('last_edit')
        students.Age = int(self.request.get('age_edit'))
        students.put()
        self.redirect('/success-edit')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/guestbook', GuestbookPage),
    ('/sign', Guestbook),
    ('/student/create',StudentCreatePage),
    ('/student/profile/(.*)',ProfilePage),
    ('/success-delete',SuccessDelete),
    ('/success-edit',SuccessEdit),
    ('/student/list',StudentList),
    ('/success-create',SuccessCreate),
    ('/student/delete/(.*)', DeletePage),
    ('/student/edit/(.*)', EditPage)
], debug=True)
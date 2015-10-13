############## 	NOTE: IMPROTANT THINGS TO DO	#################
#	API FOR OTHER CRUDS											#
#	FIX CRUD FOR CREATE											#
#	PROVIDE FRAMEWORK FOR USER/ADMIN STRUCTURE					#
#	STREAMLINE SITE MAP											#
#	FOR LOOP ON THESIS CREATE									#
#							OPTIONAL:							#
#	FIX NDB MODELS	/											#
#	ENHANCE TAGGING												#
#	ENHANCE SEARCH WITH FREQUENCY								#
#################################################################


import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json
import time
import csv
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

##### PROJECT MODELS #####

class User(ndb.Model):
	email=ndb.StringProperty(indexed=True)
	first_name=ndb.StringProperty()
	last_name=ndb.StringProperty()
	current_date=ndb.DateTimeProperty(auto_now_add=True)
	
class Thesis(ndb.Model):
	year=ndb.IntegerProperty()
	title=ndb.StringProperty()
	#~ abstract=ndb.StringProperty()
	abstract=ndb.TextProperty()
	section=ndb.IntegerProperty()
	adviser=ndb.KeyProperty()#faculty_key
	members=ndb.KeyProperty(repeated=True)#student_key and faculty_key
	#~ members=ndb.StringProperty()#student_key and faculty_key
	created_by=ndb.StringProperty()
	department=ndb.KeyProperty()#department_key
	tags=ndb.StringProperty(repeated=True)
	date=ndb.DateTimeProperty(auto_now_add=True)

class Faculty(ndb.Model):
	title=ndb.StringProperty()
	first_name=ndb.StringProperty()
	last_name=ndb.StringProperty()
	email=ndb.StringProperty()
	phone_number=ndb.StringProperty()
	birthdate=ndb.StringProperty()
	picture=ndb.StringProperty()
	department=ndb.KeyProperty()#department_key
	created_by=ndb.StringProperty()
	
	@classmethod
	def get_by_name(cls, adviser_name):
		try:
			return ndb.Key(cls, adviser_name).get()
		except:
			return None

class Student(ndb.Model):
	first_name=ndb.StringProperty()
	last_name=ndb.StringProperty()
	name=ndb.StringProperty()
	email=ndb.StringProperty()
	phone_number=ndb.StringProperty()
	birthdate=ndb.StringProperty()
	picture=ndb.StringProperty()
	year_graduated=ndb.StringProperty()
	department=ndb.KeyProperty()#department_key
	created_by=ndb.StringProperty()
			
class University(ndb.Model):
	name=ndb.StringProperty()
	address=ndb.StringProperty()
	initials=ndb.StringProperty()
	created_by=ndb.StringProperty()
	
class College(ndb.Model):
	university_key=ndb.KeyProperty()#university_key
	name=ndb.StringProperty()
	departments=ndb.KeyProperty()
	created_by=ndb.StringProperty()
	
class Department(ndb.Model):
	college_key=ndb.KeyProperty()#college_key
	name=ndb.StringProperty()
	chairperson=ndb.StringProperty()#faculty_key
	created_by=ndb.StringProperty()
	
	@classmethod
	def get_department(cls, dept, college, uni):
		university = University.query(University.name==uni).get()
		college = College.query(College.university_key==university.key).get()
		return cls.query(cls.college_key==college.key).get()
	
##### END OF PROJECT MODELS #####

##### UTILITY FUNCTIONS #####

def Render_Page(self):
	loggedin_user = users.get_current_user()
	if loggedin_user:
		user_key= ndb.Key('User', loggedin_user.user_id())
		user = user_key.get()
		if user: 
			template_values = {
				'logout_url': users.create_logout_url('/'),
				'upload_url' : blobstore.create_upload_url('/upload'),
				'loggedin_user': "%s %s" % (user.first_name, user.last_name)
			}
			return template_values
		else:
			self.redirect('/register')
	else:
		self.redirect(users.create_login_url('/register'))

def Process_CSV(blob_info):
    blob_reader = blobstore.BlobReader(blob_info.key())
    reader = csv.DictReader(blob_reader, delimiter=',')
    uni = University(name='Polytechnic University of the Philippines', initials='PUP')
    uni.put()
    
    college = College(name='Engineering', university_key=uni.key)
    college.put()
    
    dept = Department(name='Computer Engineering', college_key=college.key)
    dept.put()
    
    for row in reader:
		user = users.get_current_user()
		tag_list = []
		title_list = row['Title'].lower().split(' ')
		thesis = Thesis(id=''.join(title_list))
		tag_list.extend(title_list)
		thesis.year = int(row['Year'])
		thesis.title = row['Title']
		thesis.abstract = row['Abstract']
		thesis.section = int(row['Section'])
		faculty = Faculty.get_by_name(row['Adviser'].lower().replace(' ', ''))
		if faculty is None:
			if len(row['Adviser']) > 0:
				faculty = Faculty(id=row['Adviser'].lower().replace(' ', ''), 
					first_name=row['Adviser'].split(' ')[0].title(),  last_name=row['Adviser'].split(' ')[1].title())
				tag_list.extend(row['Adviser'].lower().split(' '))
			else:
				faculty = Faculty(id='Anonymous')
			faculty.put()
			thesis.adviser = faculty.key
		else:
			tag_list.extend(row['Adviser'].lower().split(' '))
			thesis.adviser = faculty.key
		member_list = [
			row['Member 1'], 
			row['Member 2'], 
			row['Member 3'], 
			row['Member 4'], 
			row['Member 5']
			]
		member_keys = []#.lower().replace(' ', '').replace(',', '').replace('.', '')
		for member in member_list:
			if member != '':
				tag_list.extend(member.lower().split(' '))
				student = Student(name=member)
				student.put()
				member_keys.append(student.key)
		for tag in tag_list:
			tag.replace('.','').replace(',','').replace(':','').replace(';','')
		thesis.members = member_keys
		dept = Department.get_department(row['Department'], row['College'], row['University'])
		thesis.tags = tag_list
		thesis.department = dept.key
		thesis.created_by = user.nickname()
		thesis.put()
		
def Lookup(words, search_term):
	words = words.split(' ')
	search_term = search_term.split(' ')
	for word in words:
		word = word.replace('.,;:~!?\\\'\"[]{}()*&^%$#@`/|=+_<>', '')#get rid of special chars (doesn't include '-')
	for term in search_term:
		term = term.replace('.,;:~!?\\\'\"[]{}()*&^%$#@`/|=+_<>', '')#get rid of special chars
	for term in search_term:
		for word in words:
			if  word.lower() == term.lower():
				return True
	return False
	
def GetMember(member_id):
	logging.info(member_id)
	try:
		return ndb.Key(urlsafe=self.request.get(member_id)).get().key
	except:
		return None
	

##### END OF UTILITY FUNCTIONS #####

##### PAGE HANDLERS #####
	
class RegisterPageHandler(webapp2.RequestHandler):
	def get(self):
		logged_in_user = users.get_current_user()
		if logged_in_user:
			user_key = ndb.Key('User', logged_in_user.user_id())
			user = user_key.get()
			if user:
				self.redirect('/')
			else:
				template_values = {
					'email': logged_in_user.nickname(),
					'logout_url': users.create_logout_url('/register')
				};
				template = JINJA_ENVIRONMENT.get_template('register.html')
				self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url('/register'))
			
	def post(self):
		loggedin_user = users.get_current_user()
		user = User(id=loggedin_user.user_id(), email=loggedin_user.email(),
			first_name = self.request.get('first_name'),
			last_name = self.request.get('last_name'))
		user.put()
		self.redirect('/')
		
class CreateThesisPageHandler(webapp2.RequestHandler):
	def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('create_thesis_page.html')
			self.response.write(template.render(template_values))
		
class EditThesisPageHandler(webapp2.RequestHandler):
	def get(self, thesis_id):
		template_values=Render_Page(self)
		if template_values > 0:
			thesis_key= ndb.Key(urlsafe=thesis_id)
			thesis = thesis_key.get()
			member_list = []
			for member in thesis.members:
				try:
					member_list.append(member.get().name)
				except:
					member_list.append("%s %s" % (member.get().first_name, member.get().last_name))
			template_values['thesis_id'] = thesis.key.urlsafe()
			template_values['or_year'] = thesis.year
			template_values['or_title'] = thesis.title
			template_values['or_abstract'] = thesis.abstract
			template_values['or_adviser'] = "%s %s" % (thesis.adviser.get().first_name, thesis.adviser.get().last_name)
			template_values['or_members'] = member_list
			template_values['or_dept'] = thesis.department.get().name
			template_values['or_tags'] = thesis.tags
			template_values['or_section'] = thesis.section
			template = JINJA_ENVIRONMENT.get_template('edit_thesis_page.html')
			self.response.write(template.render(template_values))
		
class SearchPageHandler(webapp2.RequestHandler):
	def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('search.html')
			self.response.write(template.render(template_values))
		
class ListIndexPageHandler(webapp2.RequestHandler):
	def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('list_index.html')
			self.response.write(template.render(template_values))
		
class ListPageHandler(webapp2.RequestHandler):
	def get(self, list_categ, list_by):
		template_values=Render_Page(self)
		if template_values > 0:
			list_categ = list_categ.title()
			if list_categ == 'All':
				template_values['list_categ'] = list_categ			
				template_values['list_by'] = ''
			elif list_categ == 'Adviser':
				template_values['list_categ'] = list_categ
				template_values['list_by'] = "%s %s" % (list_by.split('_')[0], list_by.split('_')[1])
			else:
				template_values['list_categ'] = list_categ
				template_values['list_by'] = list_by.replace('_', ' ')
			template = JINJA_ENVIRONMENT.get_template('list.html')
			self.response.write(template.render(template_values))
		

class CreateFacultyPageHandler(webapp2.RequestHandler):
	def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('create_faculty.html')
			self.response.write(template.render(template_values))
			
class CreateStudentPageHandler(webapp2.RequestHandler):
	def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('create_student.html')
			self.response.write(template.render(template_values))

class CreateUnivPageHandler(webapp2.RequestHandler):
	def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('create_ucd.html')
			self.response.write(template.render(template_values))
			
class CreateCollegePageHandler(webapp2.RequestHandler):
	def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('create_ucd.html')
			self.response.write(template.render(template_values))
			
class CreateDeptPageHandler(webapp2.RequestHandler):
	def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('create_ucd.html')
			self.response.write(template.render(template_values))
		
class DetailsPageHandler(webapp2.RequestHandler):
	def get(self, thesis_id):
		template_values=Render_Page(self)
		if template_values > 0:
			thesis_key= ndb.Key(urlsafe=thesis_id)
			thesis = thesis_key.get()
			member_list = []
			member_list_keys = []
			for member in thesis.members:
				try:
					member_list_keys.append(member.get().key.urlsafe())
					member_list.append(member.get().name)
				except:
					member_list_keys.append(member.get().key.urlsafe())
					member_list.append("%s %s" % (member.get().first_name, member.get().last_name))
			template_values['thesis_id'] = thesis.key.urlsafe()
			template_values['d_year'] = thesis.year
			template_values['d_title'] = thesis.title
			template_values['d_abstract'] = thesis.abstract
			template_values['d_adviser'] = "%s %s" % (thesis.adviser.get().first_name, thesis.adviser.get().last_name)
			template_values['d_adviser_id'] = thesis.adviser.get().key.urlsafe()
			#~ template_values['d_members'] = member_list
			#~ template_values['d_members_keys'] = member_list_keys
			template_values['d_dept'] = thesis.department.get().name
			template_values['d_college'] = thesis.department.get().college_key.get().name
			template_values['d_university'] = thesis.department.get().college_key.get().university_key.get().name
			template_values['d_section'] = thesis.section
			template_values['d_tags'] = thesis.tags
			template_values['d_created_by'] = thesis.created_by
			template_values['d_created_on'] = thesis.date
			template = JINJA_ENVIRONMENT.get_template('details.html')
			self.response.write(template.render(template_values))
		
class UploadPageHandler(blobstore_handlers.BlobstoreUploadHandler):
	def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('upload.html')
			self.response.write(template.render(template_values))
		
	def post(self):
		upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
		blob_info = upload_files[0]
		Process_CSV(blob_info)

		blobstore.delete(blob_info.key())  # optional: delete file after import
		self.redirect('/')

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
		template_values=Render_Page(self)
		if template_values > 0:
			template = JINJA_ENVIRONMENT.get_template('main.html')
			self.response.write(template.render(template_values))
		
        
##### END OF PAGE HANDLERS #####

##### API CLASSES #####	

class ThesisEntryAPI(webapp2.RequestHandler):
	def get(self):
		thesis = Thesis.query().order(Thesis.date).fetch()
		thesis_list = []
		
		for t in thesis:
			thesis_list.append({
				'id':t.key.urlsafe(),
                'year': t.year,
                'title': t.title,
                'abstract': t.abstract,
                #~ 'section': t.section,
                #~ 'adviser': t.adviser,
                #~ 'members': t.members,
                #~ 'department': t.department,
                'created_by':t.created_by	
			})
			
		response = {
			'result': 'OK',
			'data': thesis_list
		}
		self.response.headers['Content-Type'] = 'app/json'
		self.response.out.write(json.dumps(response))
        
	def post(self):
		thesis = Thesis(id = self.request.get('title').lower().replace(' .,;:~!?\\\'\"[]{}()*&^%$#@`/|=+-_<>', ''))
		thesis.year = int(self.request.get('year'))
		thesis.title = self.request.get('title')
		thesis.abstract = self.request.get('abstract')
		thesis.section = int(self.request.get('section'))
		thesis.adviser = ndb.Key(urlsafe=self.request.get('adviser')).get().key
		member_id_list = []
		for i in range (0, 4):
			try:
				member_id_list.append(ndb.Key(urlsafe=self.request.get(("%s%s" %('members', str(i))))).get().key)
			except:
				break
		for i in range (0, 50):
			try:
				tag_list.append(ndb.Key(urlsafe=self.request.get(("%s%s" %('tags', str(i))))).get().key)
			except:
				break
		thesis.members = member_id_list
		thesis.department = ndb.Key(urlsafe=self.request.get('department')).get().key
		thesis.tags = tag_list
		thesis.created_by = users.get_current_user().nickname()
		thesis.put()
		time.sleep(0.1)
		self.redirect('/thesis/create')

		#~ self.response.headers['Content-Type'] = 'app/json'
		#~ response = {
			#~ 'result': 'OK',
			#~ 'data': {
				#~ 'id':thesis.key.urlsafe(),
				#~ 'year': thesis.year,
				#~ 'title': thesis.title,
				#~ 'abstract': thesis.abstract,
				#~ 'section': thesis.section,
				#~ 'adviser': thesis.adviser,
				#~ 'members': thesis.members,
				#~ 'department': thesis.department,
				#~ 'created_by':thesis.created_by
			#~ }
		#~ }
#~ 
		#~ self.response.out.write(json.dumps(response))
		
class DeleteEntryAPI(webapp2.RequestHandler):
	def get(self, thesis_id):
		thesis_key = ndb.Key(urlsafe=thesis_id)
		thesis = thesis_key.get()
		thesis.key.delete()
		time.sleep(0.1)
		self.redirect('/thesis/create')
		
class ProponentsAPI(webapp2.RequestHandler):
	def get(self, thesis_id):
		thesis_key = ndb.Key(urlsafe=thesis_id)
		thesis = thesis_key.get()
		student_list = []
		for member in thesis.members:
			student_list.append({
				'student_name': member.get().name,
				'student_id': member.get().key.urlsafe()
			})
		response = {
			'result': 'OK',
			'students': student_list
		}
		self.response.headers['Content-Type'] = 'app/json'
		self.response.out.write(json.dumps(response))
        
class EditEntryAPI(webapp2.RequestHandler):
	def post(self, thesis_id):
		thesis_key = ndb.Key(urlsafe = thesis_id)
		thesis = thesis_key.get() 
		thesis.year = int(self.request.get('year'))
		thesis.title = self.request.get('title')
		thesis.abstract = self.request.get('abstract')
		thesis.section = int(self.request.get('section'))
		thesis.adviser = ndb.Key(urlsafe=self.request.get('adviser')).get().key
		member_id_list = []
		tag_list = []
		for i in range (0, 4):
			try:
				member_id_list.append(ndb.Key(urlsafe=self.request.get(("%s%s" %('members', str(i))))).get().key)
			except:
				break
		for i in range (0, 50):
			try:
				tag_list.append(ndb.Key(urlsafe=self.request.get(("%s%s" %('tags', str(i))))).get().key)
			except:
				break
		thesis.members = member_id_list
		thesis.department = ndb.Key(urlsafe=self.request.get('department')).get().key
		thesis.tags = tag_list
		thesis.created_by = users.get_current_user().nickname()
		thesis.put()
		self.redirect('/')
		
		#~ self.response.headers['Content-Type'] = 'app/json'
		#~ response = {
			#~ 'result': 'OK',
			#~ 'data': {
				#~ 'id':thesis.key.urlsafe(),
				#~ 'year': thesis.year,
				#~ 'title': thesis.title,
				#~ 'abstract': thesis.abstract,
				#~ 'section': thesis.section,
				#~ 'adviser': thesis.adviser,
				#~ 'members': thesis.members,
				#~ 'department': thesis.department,
				#~ 'created_by':thesis.created_by
			#~ }
		#~ }
		#~ self.response.out.write(json.dumps(response))
		#~ self.redirect('/thesis/create')
		
class FormFillAPI(webapp2.RequestHandler):
	def get(self):
		faculty = Faculty.query().fetch()
		department = Department.query().fetch()
		college = College.query().fetch()
		university = University.query().fetch()
		student = Student.query().fetch()
		adviser_list = []
		student_list = []
		department_list = []
		university_list = []
		college_list = []
		
		for f in faculty:
			if "%s %s" % (f.first_name, f.last_name) not in adviser_list:
				adviser_list.append({
					'adviser_name': "%s %s" % (f.first_name, f.last_name),
					'adviser_id': f.key.urlsafe()
				})
		for d in department:
			if d.name not in department_list:
				department_list.append({
					'dept_name': d.name,
					'dept_id': d.key.urlsafe()
				})
		for c in college:
			if c.name not in college_list:
				college_list.append({
					'coll_name': c.name,
					'coll_id': c.key.urlsafe()
				})
		for u in university:
			if u.name not in university_list:
				university_list.append({
					'univ_name': u.name,
					'univ_id': u.key.urlsafe()
				})
		for s in student:
			if s.name not in student_list:
				student_list.append({
					'student_name': s.name,
					'student_id': s.key.urlsafe()
				})
			
		response = {
			'result': 'OK',
			'advisers': adviser_list,
			'departments': department_list,
			'colleges': college_list,
			'universities': university_list,
			'students': student_list
		}
		self.response.headers['Content-Type'] = 'app/json'
		self.response.out.write(json.dumps(response))

class SearchAPI(webapp2.RequestHandler):
	def get(self, search_term):
		thesis = Thesis.query(Thesis.tags.IN([search_term]))
		thesis_list = []
		for t in thesis:
			thesis_list.append({
				'id':t.key.urlsafe(),
				'year': t.year,
				'title': t.title,
				#~ 'abstract': t.abstract,
				#~ 'section': t.section,
				#~ 'adviser': "%s %s" % (t.adviser.get().first_name, t.adviser.get().last_name),
				#~ 'members': t.members,
				#~ 'department': t.department.get().name,
				'created_by':t.created_by
			})
		response = {
			'result': 'OK',
			'data': thesis_list
		}
		self.response.headers['Content-Type'] = 'app/json'
		self.response.out.write(json.dumps(response))
		
class ListThesisAPI(webapp2.RequestHandler):
	def get(self, list_categ, list_item ):
		thesis = Thesis.query().order(Thesis.year).fetch()
		thesis_list = []
		toPrint = False
		logging.info(list_item)
		for t in thesis:
			if list_categ == 'All':
				toPrint = True
			elif list_categ == 'Year':
				if int(list_item) == t.year:
					toPrint = True
			elif list_categ == 'University':
				if list_item == t.department.get().college_key.get().university_key.get().name:
					toPrint = True
			elif list_categ == 'Adviser':
				if list_item == "%s_%s" % (t.adviser.get().first_name, t.adviser.get().last_name):
					toPrint = True
			if toPrint:
				thesis_list.append({
					'id':t.key.urlsafe(),
					'year': t.year,
					'title': t.title,
					#~ 'abstract': t.abstract,
					#~ 'section': t.section,
					#~ 'adviser': "%s %s" % (t.adviser.get().first_name, t.adviser.get().last_name),
					#~ 'members': str(t.members),
					#~ 'department': t.department,
					'created_by':t.created_by
				})
				toPrint = False
	
		response = {
			'result': 'OK',
			'data': thesis_list
		}
		self.response.headers['Content-Type'] = 'app/json'
		self.response.out.write(json.dumps(response))
		
class ListIndexAPI(webapp2.RequestHandler):
	def get(self):
		thesis = Thesis.query().fetch()
		thesis_list_adviser = []
		thesis_list_university = []
		
		for t in thesis:
			if "%s_%s" % (t.adviser.get().first_name, t.adviser.get().last_name) not in thesis_list_adviser:
				thesis_list_adviser.append("%s_%s" % (t.adviser.get().first_name, t.adviser.get().last_name) )
				
			if t.department.get().college_key.get().university_key.get().name.replace(' ', '_') not in thesis_list_university:
				thesis_list_university.append(t.department.get().college_key.get().university_key.get().name.replace(' ', '_'))
				
		response = {
			'result': 'OK',
			'adviser': thesis_list_adviser,
			'university': thesis_list_university
		}
		self.response.headers['Content-Type'] = 'app/json'
		self.response.out.write(json.dumps(response))

class RelatedThesisAPI(webapp2.RequestHandler):
	def get(self, thesis_id):
		related_key = ndb.Key(urlsafe=thesis_id)
		tag_list = []
		for tag in related_key.get().tags:
			tag_list.extend(tag)
		thesis = Thesis.query(Thesis.tags.IN(tag_list)).fetch(5)
		
		#~ search_term = "%s" % (related_key.get().title)
		#~ page_key = related_key.get().key
		#~ thesis = Thesis.query().fetch(10)

		thesis_list = []
		for  t in thesis:
			#~ if t.key != page_key and Lookup(t.title, search_term): #Lookup(t.tags, search_term) or
			thesis_list.append({
				'id':t.key.urlsafe(),
				'year': t.year,
				'title': t.title,
				'abstract': t.abstract,
				#~ 'section': t.section,
				#~ 'adviser': t.adviser,
				#~ 'members': t.members,
				#~ 'department': t.department,
				'created_by':t.created_by
			})
		response = {
			'result': 'OK',
			'data': thesis_list
		}
		self.response.headers['Content-Type'] = 'app/json'
		self.response.out.write(json.dumps(response))
		
class FacultyAPI(webapp2.RequestHandler):
	def post(self):
		faculty = Faculty()
		faculty.id=self.request.get('first_name').lower() + self.request.get('last_name').lower()
		faculty.first_name = self.request.get('first_name')
		faculty.last_name = self.request.get('last_name')
		faculty.email = self.request.get('email')
		faculty.phone_number = self.request.get('phone_number')
		faculty.birthdate = self.request.get('birthdate')
		faculty.department = ndb.Key(urlsafe=self.request.get('department')).get().key
		faculty.created_by = users.get_current_user().nickname()
		faculty.put()
		self.redirect('/faculty/create')
		
		
class DeleteFacultyAPI(webapp2.RequestHandler):
	def get(self, faculty_id):
		faculty_key = ndb.Key(urlsafe=faculty_id)
		faculty = faculty_key.get()
		faculty.key.delete()
		time.sleep(0.1)
		self.redirect('/')
		
class StudentAPI(webapp2.RequestHandler):
	def post(self):
		student = Student()
		student.first_name = self.request.get('first_name')
		student.last_name = self.request.get('last_name')
		student.name = "%s %s" % (self.request.get('first_name').lower(), self.request.get('last_name').lower())
		student.email = self.request.get('email')
		student.phone_number = self.request.get('phone_number')
		student.birthdate = self.request.get('birthdate')
		student.department = ndb.Key(urlsafe=self.request.get('department')).get().key
		student.created_by = users.get_current_user().nickname()
		student.put()
		self.redirect('/student/create')

class DeleteStudentAPI(webapp2.RequestHandler):
	def get(self, student_id):
		student_key = ndb.Key(urlsafe=student_id)
		student = student_key.get()
		student.key.delete()
		time.sleep(0.1)
		self.redirect('/')
		
class UniversityAPI(webapp2.RequestHandler):
	def post(self):
		university = University()
		university.id= self.request.get('name').lower().replace(' .,;:~!?\\\'\"[]{}()*&^%$#@`/|=+-_<>', '')
		university.name = self.request.get('name')
		university.address = self.request.get('address')
		university.initials = self.request.get('initials')
		university.created_by = users.get_current_user().nickname()
		university.put()
		self.redirect('/university/create')
		
class DeleteUniversityAPI(webapp2.RequestHandler):
	def get(self, university_id):
		university_key = ndb.Key(urlsafe=university_id)
		university = university_key.get()
		university.key.delete()
		time.sleep(0.1)
		self.redirect('/')
		
class CollegeAPI(webapp2.RequestHandler):
	def post(self):
		college = College()
		college.university_key = ndb.Key(urlsafe=self.request.get('university')).get().key
		college.name = self.request.get('name')
		college.created_by = users.get_current_user().nickname()
		college.put()
		self.redirect('/college/create')
		
class DeleteCollegeAPI(webapp2.RequestHandler):
	def get(self, college_id):
		college_key = ndb.Key(urlsafe=college_id)
		college = college_key.get()
		college.key.delete()
		time.sleep(0.1)
		self.redirect('/')
		
class DepartmentAPI(webapp2.RequestHandler):
	def post(self):
		department = Department()
		department.college_key =  ndb.Key(urlsafe=self.request.get('college')).get().key
		department.name = self.request.get('name')
		department.chairperson = self.request.get('chairperson')#ndb.Key(urlsafe=self.request.get('chairperson')).get().key
		department.created_by = users.get_current_user().nickname()
		department.put()
		self.redirect('/department/create')
		
class DeleteDepartmentAPI(webapp2.RequestHandler):
	def get(self, department_id):
		department_key = ndb.Key(urlsafe=department_id)
		department = department_key.get()
		department.key.delete()
		time.sleep(0.1)
		self.redirect('/')

##### END OF API CLASSES #####
        
app = webapp2.WSGIApplication([
    ('/register', RegisterPageHandler),
    ('/thesis/details/(.*)', DetailsPageHandler),
    ('/thesis/index', ListIndexPageHandler),
    ('/thesis/list/(.*)/(.*)', ListPageHandler),
    ('/thesis/create', CreateThesisPageHandler),
    ('/thesis/edit/(.*)', EditThesisPageHandler),
    ('/search', SearchPageHandler),
    ('/faculty/create', CreateFacultyPageHandler),
    ('/student/create', CreateStudentPageHandler),
    ('/university/create', CreateUnivPageHandler),
    ('/college/create', CreateCollegePageHandler),
    ('/department/create', CreateDeptPageHandler),
	('/api/thesis/list/(.*)/(.*)', ListThesisAPI),
    ('/api/thesis/search/(.*)', SearchAPI),
    ('/api/thesis/delete/(.*)', DeleteEntryAPI),
    ('/api/thesis/edit/(.*)', EditEntryAPI),
    ('/api/thesis/related/(.*)', RelatedThesisAPI),
    ('/api/thesis/proponents/(.*)', ProponentsAPI),
    ('/api/student/delete/(.*)', DeleteStudentAPI),
    ('/api/faculty/delete/(.*)', DeleteFacultyAPI),
    ('/api/university/delete/(.*)', DeleteUniversityAPI),
    ('/api/college/delete/(.*)', DeleteCollegeAPI),
    ('/api/department/delete/(.*)', DeleteDepartmentAPI),
    ('/api/thesis/index', ListIndexAPI),
    ('/api/thesis/form', FormFillAPI),
    ('/api/thesis', ThesisEntryAPI),
    ('/api/student', StudentAPI),
    ('/api/faculty', FacultyAPI),
    ('/api/university', UniversityAPI),
    ('/api/college', CollegeAPI),
    ('/api/department', DepartmentAPI),
    ('/upload', UploadPageHandler),
    ('/', MainPageHandler)
], debug=True)

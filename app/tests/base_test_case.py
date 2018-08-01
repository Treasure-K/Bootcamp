from flask_testing import TestCase
from flask import Flask
from app import app
import json
from app.users.views import users


class BaseTestCase(TestCase):


	token = ""


	def create_app(self):
		app = Flask(__name__)
		return app


	def setUp(self):
		self.client = app.test_client(self)


	def tearDown(self):
		users[:] = []
		token = ""

	
	def signup(self, user_data = json.dumps(dict(
			first_name = "Treasure",
			last_name = "Kabareebe",
			email = "ab@hotmail.com",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))):
		response = self.client.post('/auth/signup',
									data=user_data,
									content_type='application/json')
		return json.loads(response.data.decode('utf-8'))


	def login(self):
		self.signup()
		login_data = json.dumps(dict(
			email = "ab@hotmail.com",
			password = "12345#tlk"
		))
		response = self.client.post('/auth/login', data=login_data, content_type='application/json') 
		self.token = json.loads(response.data.decode('utf-8'))["token"]
		return self.token


	@staticmethod
	def create_entry():
		return json.dumps(dict(
			entry_title="Test",
			entry_date="2004-04-04",
			entry_content= "This is a test"
		))


	def add_entry(self):
		token = self.login()
		entry_data = self.create_entry()
		response = self.client.post('/entries', data=entry_data, headers={'token':token}, content_type='application/json')
		return {
			"token": token,
			"json_data": json.loads(response.data.decode('utf-8'))
		} 


	def get_entries(self):
		token = self.add_entry()["token"]
		response = self.client.get('/entries',
									headers={'token':token},
									content_type='application/json')
		return json.loads(response.data.decode('utf-8'))["entries"]


	def get_entry(self):
		entries = self.get_entries()
		return entries[0]

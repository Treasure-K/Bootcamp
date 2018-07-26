from flask_testing import TestCase
from flask import Flask
from app import app
import json

class TestEntriesEndpoints(TestCase):

	def create_app(self):
		app = Flask(__name__)
		return app

	def setUp(self):
		self.client = app.test_client(self)

	@staticmethod
	def create_user():
		return json.dumps(dict(
			first_name = "Treasure",
			last_name = "Kabareebe",
			email = "ab@hotmail.com",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))

	@staticmethod
	def create_entry():
		return json.dumps(dict(
			entry_title="Test",
			entry_date="2004-04-04",
			entry_content= "This is a test"
		))

	def register_user(self):
		""" """
		user_data = self.create_user()
		self.client.post('/auth/signup', data=user_data, content_type='application/json')

	def login_user(self):
		self.register_user()
		user_data = self.create_user()
		response = self.client.post('/auth/login', data=user_data, content_type='application/json')
		return json.loads(response.data.decode('utf-8'))["token"]

	def test_create_entry(self):
		token = self.login_user()
		entry_data = self.create_entry()
		response = self.client.post('/entries', data=entry_data,
						 headers={'token':token},
						 content_type='application/json')
		json_response = json.loads(response.data.decode('utf-8'))
		self.assertEqual(json_response["message"], "Entry added successfully")

from flask_testing import TestCase
from flask import Flask
from app import app
import json

class TestAuthEndpoints(TestCase):

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

	def test_user_register_successful(self):
		""" """
		user_data = self.create_user()
		response = self.client.post('/auth/signup', data=user_data, content_type='application/json')
		json_response = json.loads(response.data.decode('utf-8'))
		self.assertEqual(json_response["message"], "User created successfully")

	def test_register_fail_no_firstname(self):
		""" """
		user_data = json.dumps(dict(
			last_name = "Kabareebe",
			email = "ab@hotmail.com",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))
		response = self.client.post('/auth/signup', data=user_data, content_type='application/json')
		json_response = json.loads(response.data.decode('utf-8'))
		self.assertEqual(json_response["message"], "first_name is required")

	def test_register_fail_invalid_firstname(self):
		""" """
		user_data = json.dumps(dict(
			first_name = ".",
			last_name = "Kabareebe",
			email = "ab@hotmail.com",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))
		response = self.client.post('/auth/signup', data=user_data, content_type='application/json')
		json_response = json.loads(response.data.decode('utf-8'))
		self.assertEqual(json_response["message"], "Enter a valid first_name")

	def test_register_fail_invalid_lastname(self):
		""" """
		user_data = json.dumps(dict(
			first_name = "Treasure",
			last_name = ".",
			email = "ab@hotmail.com",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))
		response = self.client.post('/auth/signup', data=user_data, content_type='application/json')
		json_response = json.loads(response.data.decode('utf-8'))
		self.assertEqual(json_response["message"], "Enter a valid last_name")

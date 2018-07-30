from app.tests.base_test_case import BaseTestCase
import json

class TestAuthEndpoints(BaseTestCase):
	
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
		return json.loads(response.data.decode('utf-8'))["token"]

	def test_user_register_successful(self):
		""" """
		json_data = self.signup()
		self.assertEqual(json_data["message"], "User created successfully")

	def test_email_already_exists(self):
		""" """
		self.signup()
		json_data = self.signup()
		self.assertEqual(json_data["message"], "Email already in use")

	def test_register_fail_no_firstname(self):
		""" """
		user_data = json.dumps(dict(
			last_name = "Kabareebe",
			email = "ab@hotmail.com",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "first_name is required")

	def test_register_fail_invalid_firstname(self):
		""" """
		user_data = json.dumps(dict(
			first_name = ".",
			last_name = "Kabareebe",
			email = "ab@hotmail.com",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "Enter a valid first_name")


	def test_register_fail_no_lastname(self):
		""" """
		user_data = json.dumps(dict(
			first_name = "Treasure",
			email = "ab@hotmail.com",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "last_name is required")


	def test_register_fail_invalid_lastname(self):
		""" """
		user_data = json.dumps(dict(
			first_name = "Treasure",
			last_name = ".",
			email = "ab@hotmail.com",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "Enter a valid last_name")


	def test_register_fail_no_email(self):
		""" """
		user_data = json.dumps(dict(
			first_name = "Treasure",
			last_name = "Kabareebe",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "email is required")


	def test_register_fail_invalid_email(self):
		""" """
		user_data = json.dumps(dict(
			first_name = "Treasure",
			last_name = "Kabareebe",
			email = "abc",
			password = "12345#tlk",
			confirm_password = "12345#tlk"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "Enter a valid email address")


	def test_register_fail_no_password(self):
		""" """
		user_data = json.dumps(dict(
			first_name = "Treasure",
			last_name = "Kabareebe",
			email = "abc",
			confirm_password = "12345#tlk"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "password is required")


	def test_register_fail_invalid_password(self):
		""" """
		user_data = json.dumps(dict(
			first_name = "Treasure",
			last_name = "Kabareebe",
			email = "abc@gmail.com",
			password = "12",
			confirm_password = "12345#tlk"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "Enter a strong password, use special characters and numbers")


	def test_register_fail_no_confirm_password(self):
		""" """
		user_data = json.dumps(dict(
			first_name = "Treasure",
			last_name = "Kabareebe",
			email = "abc@gmail.com",
			password = "12345#tlk"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "confirm_password is required")


	def test_register_fail_invalid_confirm_password(self):
		""" """
		user_data = json.dumps(dict(
			first_name = "Treasure",
			last_name = "Kabareebe",
			email = "abc@gmail.com",
			password = "12345#tlk",
			confirm_password = "12"
		))
		json_data = self.signup(user_data)
		self.assertEqual(json_data["message"], "Passwords do not match")


	def test_login(self):
		self.signup()
		login_data = json.dumps(dict(
			email = "abc@gmail.com"
		))
		response = self.client.post('/auth/login', data=login_data, content_type='application/json') 
		json_data = json.loads(response.data.decode('utf-8'))
		self.assertEqual(json_data["message"], "password is required")

	def test_email_password_mismatch(self):
		""" """
		self.signup()
		login_data = json.dumps(dict(
			email = "ab@hotmail.com",
			password = "12345#tlked"
		))
		response = self.client.post('/auth/login', data=login_data, content_type='application/json') 
		json_data = json.loads(response.data.decode('utf-8'))
		self.assertEqual(json_data["message"], "Email and password mismatch")

	def test_user_not_found(self):
		""" """
		self.signup()
		login_data = json.dumps(dict(
			email = "ab@gmail.com",
			password = "12345#tlk"
		))
		response = self.client.post('/auth/login', data=login_data, content_type='application/json') 
		json_data = json.loads(response.data.decode('utf-8'))
		self.assertEqual(json_data["message"], "User not found")
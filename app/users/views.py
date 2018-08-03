from flask import jsonify, request, Blueprint
import re
import jwt
from passlib.hash import sha256_crypt #For encrypting passwords
import uuid
from datetime import datetime, timedelta
from app import app, cur


USERS_BLUEPRINT = Blueprint(
    'users', __name__
)

# model functions
# get all users
def get_all_users():
	sql = "SELECT * FROM users"
	cur.execute(sql)
	results = cur.fetchall()
	print('result', results)

	users = []
	for row in results:
		users.append(
			{
				"id": row[0],
				"first_name":row[1],
				"last_name":row[2],
				"email": row[3],
			}
		)
	return users

# get user by email
def get_user_by_email(email):
	cur.execute("SELECT * FROM users WHERE email = %s", (email,))
	result = cur.fetchone()
	return {
		"id": result[0],
		"first_name":result[1],
		"last_name":result[2],
		"email": result[3],
		"password": result[4]
	}

# quick check if email exists
def email_exists(email):
	cur.execute("SELECT email FROM users WHERE email = %s", (email,))
	return cur.fetchone() is not None


# Auth routes
@USERS_BLUEPRINT.route("/auth/signup", methods=['GET', 'POST'])
def sign_up():
	if request.method == "POST":
		# get request data
		data = request.get_json()
		# validate user data
		required_fields = [
			"first_name",
			"last_name",
			"email",
			"password",
			"confirm_password"
		]

		result = validate_data(data, required_fields)

		if not result["success"]:
			return jsonify(result), 400

		# check if email exists
		if email_exists(data["email"]):
			return jsonify({
			"success": False,
			"message": "Email already in use"
			}), 409


		# # form user object
		sql = "INSERT INTO users(first_name, last_name, email, password)\
		        VALUES (%s, %s, %s, %s)"
		cur.execute(
			sql, (
				data["first_name"],
				data["last_name"],
				data["email"],
				sha256_crypt.encrypt(data["password"])
			)
		)


		return jsonify({
			"success": True,
			"message": "User created successfully"
		})

	return jsonify({
		"success": True,
		"users": get_all_users()
	})


@USERS_BLUEPRINT.route("/auth/login", methods=['POST'])
def login():
	# get request data
	data = request.get_json()
	# validate user data
	required_fields = [
		"email",
		"password"
	]

	result = validate_data(data, required_fields)

	if not result["success"]:
		return jsonify(result)

	# check for user
	if not email_exists(data["email"]):
		return jsonify({
			"success": False,
			"message": "User not found"
		})

	# get user
	user = get_user_by_email(data["email"])

	# check if passwords match
	if sha256_crypt.verify(data["password"], user["password"]):
		token = jwt.encode({
			"id": user["id"],
			"exp": datetime.utcnow() + timedelta(minutes=120),
		}, 'secret_key', 'HS256')
		return jsonify({
			"success": True,
			"token": token.decode('UTF-8')
		}), 200

	return jsonify({
		"success": False,
		"message": "Email and password mismatch"
	}), 400


# helper functions
def validate_name(data, field):
	if field in data:
		if not bool(re.match('^([A-Za-z]{3,25}$)', data[field])):
			return {
				"success": False,
				"message": "Enter a valid " + field
			}
		return {
			"success": True
		}


def validate_data(data, required_fields):
	# check for required fields
	for field in required_fields:
		if field not in data:
			return {
				"success": False,
				"message": field + " is required"
			}

	# validate input
		if "first_name" in data:
			result = validate_name(data, "first_name")

			if not result["success"]:
				return result

			if "last_name" in data:
				result = validate_name(data, "last_name")
	
			if not result["success"]:
				return result

		if "email" in data:
			if not bool(re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', data["email"])):
				return {
					"success": False,
					"message": "Enter a valid email address"
				}

		if "password" in data:
			if not re.match('^[A-Za-z0-9@#$%^&+=]{8,}', data["password"]):
				return {
					"success": False,
					"message": "Enter a strong password, use special characters and numbers"
				}

		if "password" and "confirm_password" in data:
			if data["password"] != data["confirm_password"]:
				return {
					"success": False,
					"message": "Passwords do not match"
				}
		return {
			"success": True
		}

from flask import jsonify, request, Blueprint
import re
import jwt
from passlib.hash import sha256_crypt
import uuid
from datetime import datetime, timedelta
from app import app

USERS_BLUEPRINT = Blueprint(
	'users', __name__
)


users = []

@USERS_BLUEPRINT.route("/users", methods=['GET', 'POST'])
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

		# form user object
		user = {
			"id": uuid.uuid4().hex,
			"first_name": data["first_name"],
			"last_name": data["last_name"],
			"email": data["email"],
			"password": sha256_crypt.encrypt(str(data["password"]))

		}
		users.append(user)
		return jsonify({
			"success": True,
			"mesasge": "User created successfully"
		}), 201
	return jsonify({
		"success": True,
		"users": users
	}), 200

@USERS_BLUEPRINT.route("/login", methods=['POST'])
def login():
	# get request data
	data = request.get_json()
	# validate user data
	required_fields = [
		"email",
		"password",
	]
	result = validate_data(data, required_fields)
	if not result["success"]:
		return jsonify(result), 400
	# check for user user
	for user in users:
		if user["email"] == data["email"]:
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
	return jsonify({
		"success": False,
		"message": "User not found"
	})


def validate_name(data, field):
	if field in data:
		if not bool(re.match('^([A-Za-z]{3,25}$)', data[field])):
			return {
				"success": False,
				"mesasge": "Enter a valid " + field
			}
	return {
		"success": True
	}

def validate_data(data, required_fields):
	# check for required fiels
	for field in required_fields:
		if field not in data:
			return {
				"success": False,
				"mesasge": field + " is required"
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
				"success":False,
			    "message": "Enter a valid email address"
			}
	if "password" in data:
		if not re.match('^[A-Za-z0-9@#$%^&+=]{8,}', data["password"]):
			return {
		    	"success":False,
		        "message": "Enter a strong password, use special characters and numbers"
		    }
	if "password" and "confirm_password" in data:
		if data["password"] != data["confirm_password"]:
			return {
				"success":False,
			    "message": "Passwords do not match"
			}
	return {
		"success": True
	}

# @app.route("", methods['POST'])

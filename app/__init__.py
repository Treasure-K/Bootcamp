from flask import Flask, jsonify, request
import datetime
import uuid
import jwt
from functools import wraps



app = Flask(__name__)

from app.users.views import USERS_BLUEPRINT , validate_data


entries = []

def authenticate(func):
	@wraps(func)
	def wrapper(*args, **kwargs):	

		if "token" in request.headers:
			token = request.headers["token"]
		else:
			token = None

		if not token:
			return jsonify({
				"success" : False,
				"message" : "Token missing in headers"
			}), 400

		decoded = decode_auth_token(token)

		if not decoded['is_valid']:
			return jsonify({
				"success" : False,
				"message" : decoded["message"]
			}), 400

		user_id = decoded["user_id"]
		return func(user_id, *args, **kwargs)
	return wrapper

@app.route("/")
def hello():
    return jsonify("Welcome to my diary!")


app.register_blueprint(USERS_BLUEPRINT)


@app.route("/entries", methods=['GET'])
@authenticate
def fetch_entries(user_id):
	user_entries = []

	for entry in entries:
		if entry["user_id"] == user_id:
			user_entries.append(entry)
	
	return jsonify({
		"success" : True,
		"entries" : entries
	}), 200


@app.route("/entries", methods=['POST'])
@authenticate
def add_entry(user_id):
	
	data = request.get_json()
	
	required_fields = [
		"entry_title",
		"entry_date",
		"entry_content"
	]

	result = validate_entry_data(data, required_fields)

	if not result["valid"]:
			return jsonify(result), 400


	entry = {
		"user_id" : user_id,
		"entry_id": uuid.uuid4().hex,
		"entry_title" : data["entry_title"],
		"entry_date" : data["entry_date"],
		"entry_content" : data["entry_content"]
	}


	entries.append(entry)
	return jsonify({
			"success": True,
			"message": "Entry added successfully"
		}), 201
	



@app.route("/entries/<entryId>", methods=['GET'])
@authenticate
def fetch_entry_details(user_id, entryId):
	for entry in entries:
		if entry["entry_id"] == entryId:
			if entry["user_id"] == user_id:
				entry["entry_title"] = data["entry_title"]
				entry["entry_date"] = data["entry_date"]
				entry["entry_content"] = data["entry_content"]
				return jsonify({
					"success" : True,
					"entry" : entry
				}), 200
			return jsonify({
				"success" : False,
				"message" : "You are not authorised to perform that action"
			}), 401 
	
	return jsonify({
		"success" : False,
		"message" : "Entry with id " + entryId + " not found"
	}), 404


@app.route("/entries/<entryId>", methods=['PUT'])
@authenticate
def update_entry(user_id, entryId):
	data = request.get_json()
	required_fields = [
		"entry_title",
		"entry_date",
		"entry_content"
	]

	result = validate_entry_data(data, required_fields)

	if not result["valid"]:
			return jsonify(result), 400


	for entry in entries:
		if entry["entry_id"] == entryId:
			if entry["user_id"] == user_id:
				entry["entry_title"] = data["entry_title"]
				entry["entry_date"] = data["entry_date"]
				entry["entry_content"] = data["entry_content"]

				return jsonify({
					"success" : True,
					"message" : "Entry updated successfully"
				}), 200

			return jsonify({
				"success" : False,
				"message" : "You are not authorised to perform that action"
			}), 401 	
	
	return jsonify({
		"success" : False,
		"message" : "Entry with id " + entryId + " not found"
	}), 404 

def is_validate_date(date):
	# Validate date format
	date_format = '%Y-%m-%d'			
	try:
		date_obj = datetime.datetime.strptime(str(date), date_format)
		return True
	except ValueError:
		return False

def validate_entry_data(data, required_fields):
	# check for required fields
	for field in required_fields:
		if field not in data:
			return {
				"valid": False,
				"mesasge": field + " is required"
			}
	
	if is_validate_date(data["entry_date"]):
		return {
			"valid": True
		}
	else:
		return {
				"valid": False,
				"message": "Incorrect data format, should be YYYY-MM-DD"
		}

	return jsonify({
			"success": True,
			"mesasge": "Entry added successfully"
		}), 201

def decode_auth_token(auth_token):
    
    try:
        payload = jwt.decode(auth_token, 'secret_key')
        return {
        	"is_valid" : True,
        	"user_id" : payload["id"]
        }

    except:
        return {
        	"is_valid": False,
        	"message": "Invalid token"
        }



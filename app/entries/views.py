from flask import jsonify, request, Blueprint
import re
import jwt
from passlib.hash import sha256_crypt #For encrypting passwords
import uuid
from datetime import datetime, timedelta
from app import app
from functools import wraps
import psycopg2
import psycopg2.extras


ENTRIES_BLUEPRINT = Blueprint(
	'entries', __name__
)


def connect_to_db():
	connection_string = "database=mydiarydb user=postgres password=trekab host=127.0.0.1 port=5432"
	print(connection_string)

	try:
		return pycopg2.connect(connection_string)
	except:
		print("Can't connect to database")


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


@ENTRIES_BLUEPRINT.route("/entries", methods=['GET'])
@authenticate
def fetch_entries(user_id):
	user_entries = []

	# conn = connect_to_db()
	# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor

	# try:
	# 	cur.execute("")
	# except:
	# 	raise e
	# conn.commit()

	for entry in entries:
		if entry["user_id"] == user_id:
			user_entries.append(entry)
	
	return jsonify({
		"success" : True,
		"entries" : user_entries
	}), 200


@ENTRIES_BLUEPRINT.route("/entries", methods=['POST'])
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
	

@ENTRIES_BLUEPRINT.route("/entries/<entryId>", methods=['GET'])
@authenticate
def fetch_entry_details(user_id, entryId):
	for entry in entries:
		if entry["entry_id"] == entryId:
			if entry["user_id"] == user_id:

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


@ENTRIES_BLUEPRINT.route("/entries/<entryId>", methods=['PUT'])
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
			# found entry to update
			if entry["user_id"] == user_id:
				# request user is entry user
				entry["entry_title"] = data["entry_title"]
				entry["entry_date"] = data["entry_date"]
				entry["entry_content"] = data["entry_content"]

				return jsonify({
					"success" : True,
					"message" : "Entry updated successfully"
				}), 200
			# request user is not entry user
			return jsonify({
				"success" : False,
				"message" : "You are not authorised to perform that action"
			}), 401 	
	
	return jsonify({
		"success" : False,
		"message" : "Entry with id " + entryId + " not found"
	}), 404 


def is_valid_date(date):
	# Validate date format
	date_format = '%Y-%m-%d'			
	try:
		date_obj = datetime.strptime(str(date), date_format)
		return True
	except ValueError:
		return False


def validate_entry_data(data, required_fields):
	# check for required fields
	for field in required_fields:
		if field not in data:
			return {
				"valid": False,
				"message": field + " is required"
			}
	
	if is_valid_date(data["entry_date"]):
		return {
			"valid": True
		}
	else:
		return {
				"valid": False,
				"message": "Incorrect date format, should be YYYY-MM-DD"
		}

	return jsonify({
			"success": True,
			"message": "Entry added successfully"
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
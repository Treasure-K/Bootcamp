from flask import Flask, jsonify, request
import datetime
import uuid
import jwt



app = Flask(__name__)

from app.users.views import USERS_BLUEPRINT , validate_data


entries = []

@app.route("/")
def hello():
    return jsonify("Welcome to my diary!")


app.register_blueprint(USERS_BLUEPRINT)


@app.route("/entries", methods=['GET'])
def fetch_entries():
	decoded = decode_auth_token(request.headers["token"])

	if not decoded['is_valid']:
		return jsonify({
			"success" : False,
			"message" : decoded["message"]
		}), 400

	ident = decoded["user_id"]

	for index in range(len(entries)):
		for ident in entries[index]:
			return jsonify(entries)
	
	return jsonify({
		"success" : False,
		"message" : ""
	}), 400


@app.route("/entries", methods=['POST'])
def add_entry():
	
	data = request.get_json()
	
	decoded = decode_auth_token(request.headers["token"])

	if not decoded['is_valid']:
		return jsonify({
			"success" : False,
			"message" : decoded["message"]
		}), 400
	required_fields = [
		"entry_title",
		"entry_date",
		"entry_content"
	]

	result = validate_entry_data(data, required_fields)

	if not result["valid"]:
			return jsonify(result), 400


	entry = {
		"user_id" : decoded["user_id"],
		"entry_id": uuid.uuid4().hex,
		"entry_title" : data["entry_title"],
		"entry_date" : data["entry_date"],
		"entry_content" : data["entry_content"]
	}


	entries.append(entry)
	print(jsonify(entries))
	return jsonify({
			"success": True,
			"message": "Entry added successfully"
		}), 201
	



@app.route("/entries/<entryId>", methods=['GET'])
def fetch_entry_details(entryId):
	decoded = decode_auth_token(request.headers["token"])

	if not decoded['is_valid']:
		return jsonify({
			"success" : False,
			"message" : decoded["message"]
		}), 400

	ident = decoded["user_id"]

	for index in range(len(entries)):
		for ident in entries[index]:
			return jsonify(entries[index]["entry_content"])
	
	return jsonify({
		"success" : False,
		"message" : ""
	}), 400


@app.route("/entries/<entryId>", methods=['PUT'])
def update_entry(entryId):
	return 

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
        print("--------",payload)

        return {
        	"is_valid" : True,
        	"user_id" : payload["id"]
        }
      
    except jwt.ExpiredSignatureError:
        return {
        	"is_valid": False,
        	"message": "Signature expired"
        }
    except jwt.InvalidTokenError:
        return {
        	"is_valid": False,
        	"message": "Invalid token"
        }


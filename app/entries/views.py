from flask import jsonify, request, Blueprint
import re
import jwt
from passlib.hash import sha256_crypt #For encrypting passwords
from datetime import datetime, timedelta
from app import app, cur
from functools import wraps


ENTRIES_BLUEPRINT = Blueprint(
    'entries', __name__
)

# model routes

def save_entry(title, date, content, user_id):
    sql = "INSERT INTO entries(entry_title, entry_date, entry_content, user_id)\
        VALUES (%s, %s, %s, %s)"
    cur.execute(
        sql, (
            title,
            date,
            content,
            user_id
        )
    )


def get_user_entries(user_id):
    sql = "SELECT * FROM entries WHERE user_id = %s"
    cur.execute(sql, (user_id,))
    results = cur.fetchall()
    print('result', results)

    entries = []
    for row in results:
        entries.append(
            {
                "user_id": row[0],
                "id": row[1],
                "content": row[2],
                "date":row[3],
                "title":row[4]
            }
        )

    return entries

# get entry by id
def get_entry_by_id(user_id, entry_id):
    sql = "SELECT * FROM entries WHERE user_id entry_id = %s %s"
    cur.execute(sql, (user_id, entry_id,))

    if cur.fetchone() is not None:
        result = cur.fetchone()
        print('result', result)

        return {
            "exists": True,
            "entry": {
                # "entry_id": result[0],
                # "entry_title":result[1],
                # "entry_date":result[2],
                # "entry_content": result[3],
                # "user_id": result[4]
            }
        }
    return {
        "exists": False
    }




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


@ENTRIES_BLUEPRINT.route("/")
def hello():
    return jsonify("Welcome to my diary!")


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

    save_entry(data["entry_title"], data["entry_date"], data["entry_content"], user_id) 

    return jsonify({
            "success": True,
            "message": "Entry added successfully"
        })
    

@ENTRIES_BLUEPRINT.route("/entries", methods=['GET'])
@authenticate
def fetch_entries(user_id):
    return jsonify({
        "success" : True,
        "entries" : get_user_entries(user_id)
    })


@ENTRIES_BLUEPRINT.route("/entries/<entryId>", methods=['GET'])
@authenticate
def fetch_entry_details(user_id, entryId):
    result = get_entry_by_id(user_id, entryId)

    if result["exists"]:
        return jsonify({
            "success" : True,
            "entry" : result["entry"]
        })
    
    return jsonify({
        "success" : False,
        "message" : "Entry with id " + entryId + " not found"
    })


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
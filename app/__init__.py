from flask import Flask, jsonify, request
import datetime
import uuid
import jwt
from functools import wraps
import psycopg2
import re


app = Flask(__name__)


# from app.users.views import USERS_BLUEPRINT 
# from app.entries.views import ENTRIES_BLUEPRINT 


# app.register_blueprint(ENTRIES_BLUEPRINT)
# app.register_blueprint(USERS_BLUEPRINT)

def create_connection():
	conn = psycopg2.connect(database="mydiarydb", user="postgres", password="trekab",
	host="127.0.0.1", port="5432")
	conn.autocommit = True
	return conn.cursor()

def create_tables(cur): 
	cur.execute("""
	        CREATE TABLE IF NOT EXISTS users (
	            user_id SERIAL PRIMARY KEY,
	            first_name VARCHAR(255) NOT NULL,
	            last_name VARCHAR(255) NOT NULL,
	            email VARCHAR(255) NOT NULL,
	            password VARCHAR(255) NOT NULL
	        	)
	        """)


	cur.execute(""" 
			CREATE TABLE IF NOT EXISTS entries (
				 user_id SERIAL NOT NULL,
				FOREIGN KEY (user_id)
	                    REFERENCES users (user_id)
	                    ON UPDATE CASCADE ON DELETE CASCADE,
			    entry_id SERIAL PRIMARY KEY,
			    entry_title VARCHAR(255) NOT NULL,
			    entry_date DATE NOT NULL,
			    entry_content VARCHAR(255) NOT NULL
			     )
	         """)

cur = create_connection()
create_tables(cur)




@app.route("/auth/signup", methods=['GET', 'POST'])
def sign_up():
	if request.method == "POST":
		# get request data
		data = request.get_json()
		# validate user data
		# required_fields = [
		# 	"first_name",
		# 	"last_name",
		# 	"email",
		# 	"password",
		# 	"confirm_password"
		# ]
		# result = validate_data(data, required_fields)
		# if not result["success"]:
		# 	return jsonify(result), 400

		# check if email exists
		

		# for row in cur.execute("""SELECT * FROM users"""):
		# 	print(row)

		# # form user object
		sql = "INSERT INTO users(first_name, last_name, email, password)\
			VALUES (%s, %s, %s, %s)"
		cur.execute(sql, (data["first_name"], data["last_name"], data["email"], data["password"]))

		# sql = "SELECT * FROM users"
		cur.execute(" SELECT * FROM \"users\" ")
		print(cur.fetchall())



		# print('result', result)


		return jsonify({
			"success": True,
			"message": "User created successfully"
		}), 201
	return jsonify({
		"success": True,
		"users": users
	}), 200

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

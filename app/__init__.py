from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import uuid
import jwt
from functools import wraps
import psycopg2
import re
from passlib.hash import sha256_crypt


app = Flask(__name__)


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


from app.users.views import USERS_BLUEPRINT
from app.entries.views import ENTRIES_BLUEPRINT


app.register_blueprint(ENTRIES_BLUEPRINT)
app.register_blueprint(USERS_BLUEPRINT)
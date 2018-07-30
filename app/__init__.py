from flask import Flask, jsonify, request
import datetime
import uuid
import jwt
from functools import wraps


app = Flask(__name__)

from app.users.views import USERS_BLUEPRINT , validate_data

from app.entries.views import ENTRIES_BLUEPRINT 

app.register_blueprint(ENTRIES_BLUEPRINT)
app.register_blueprint(USERS_BLUEPRINT)
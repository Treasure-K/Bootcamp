from flask import Flask


app = Flask(__name__)

from app.users.views import USERS_BLUEPRINT




@app.route("/")
def hello():
    return jsonify("Welcome to my diary!")

app.register_blueprint(USERS_BLUEPRINT)

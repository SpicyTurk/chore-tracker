from config import app, db
from models import User, Chore, Complete
from flask import request, session

@app.route("/")
def index():
	return {"message": "Chore Tracker api is running"}

@app.route("/signup", methods=["POST"])
def signup():
	data = request.get_json()
	username = data.get("username")
	password = data.get("password")

	if not username or not password:
		return {"error": "Username and password are required"}, 400
	
	if User.query.filter_by(username=username).first():
		return {"error": "Username already taken"}, 409
	
	user = User(username=username)
	user.set_password(password)
	db.session.add(user)
	db.session.commit()

	session["user_id"] = user.id
	return {"id": user.id, "username": user.username}, 201
	

if __name__ == "__main__":
	app.run(port=5555, debug=True)

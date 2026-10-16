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

@app.route("/login", methods=["POST"])
def login():
	data = request.get_json()
	user = User.query.filter_by(username=data.get("username")).first()

	if user and user.check_password(data.get("password", "")):
		session["user_id"] = user.id
		return {"id": user.id, "username": user.username}, 200
	return {"error": "Invalid username or password"}, 401

@app.route("/logout", methods=["DELETE"])
def logout():
	session.pop("user_id", None)
	return {}, 204

@app.route("/check_session")
def check_session():
	user_id = session.get("user_id")
	if not user_id:
		return {"error": "Not logged in"}, 401

	user = db.session.get(User, user_id)
	if not user:
		return {"error": "Not logged in"}, 401

	return {"id": user.id, "username":user.username}, 200




if __name__ == "__main__":
	app.run(port=5555, debug=True)

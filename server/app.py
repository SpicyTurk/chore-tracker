from config import app, db
from models import User, Chore, Complete
from flask import request, session
from datetime import date
from sqlalchemy import or_

def current_user():
	user_id = session.get("user_id")
	if not user_id:
		return None
	return db.session.get(User, user_id)


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

@app.route("/chores", methods=["POST"])
def create_chore():
	user = current_user()
	if not user:
		return {"error": "Must be logged in to create a new chore"}, 401

	data = request.get_json()
	title = data.get("title")
	due_date_text = data.get("due")
	assignee_username = data.get("assignee")

	if not title or not due_date_text or not assignee_username:
		return {"error": "A title, due date and assignee are required"}, 400
	try:
		due = date.fromisoformat(due_date_text)
	except ValueError:
		return {"error": "Date must be in the format YYYY-MM-DD"}, 400

	assignee = User.query.filter_by(username=assignee_username).first()
	if not assignee:
		return {"error": "No user named " + assignee_username}, 404

	chore = Chore(title=title, due_date=due, creator=user, assignee=assignee)
	db.session.add(chore)
	db.session.commit()
	return chore.to_dict(), 201

@app.route("/chores", methods=["GET"])
def list_chores():
	user = current_user()
	if not user:
		return {"error": "Please login to view chore history"}, 401

	page = request.args.get("page", 1, type=int)
	per_page = request.args.get("per_page", 10, type=int)
	per_page = min(per_page, 30)

	query = Chore.query.filter(
		or_(Chore.creator_id == user.id, Chore.assignee_id == user.id)
	).order_by(Chore.due_date.asc(), Chore.id.asc())

	result = query.paginate(page=page, per_page=per_page, error_out=False)

	return {
		"chores": [c.to_dict() for c in result.items],
		"page": result.page,
		"per_page": per_page,
		"total": result.total,
		"pages": result.pages,
	}, 200

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

@app.route("/chores/<int:chore_id>", methods=["PATCH"])
def update_chore(chore_id):
	user = current_user()
	if not user:
		return {"error": "Please log in first"}, 401

	chore = db.session.get(Chore, chore_id)
	if not chore:
		return {"error": "Chore not found"}, 404

	if chore.creator_id != user.id:
		return {"error": "Only the owner can edit this chore"}, 403

	if chore.completion:
		return {"error": "Completed chores cannot be edited"}, 409

	data = request.get_json()

	if "title" in data:
		if not data["title"]:
			return {"error": "Title cannot be empty"}, 400
		chore.title = data["title"]

	if "due_date" in data:
		try:
			chore.due_date = date.fromisoformat(data["due_date"])
		except ValueError:
			return {"error": "Date must be in the format of YYYY-MM-DD"}, 400

	db.session.commit()
	return chore.to_dict(), 200


if __name__ == "__main__":
	app.run(port=5555, debug=True)

from config import app, db
from models import User, Chore, Complete


@app.route("/")
def index():
	return {"message": "Chore Tracker api is running"}


if __name__ == "__main__":
	app.run(port=5555, debug=True)

from config import db, bcrypt 
from datetime import datetime

password_hash = db.Column(db.String, nullable=False)

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)

	def set_password(self, password):
		self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

	def check_password(self, password):
		return bcrypt.check_password_hash(self.password_hash, password)

	created_chores = db.relationship("Chore", foreign_keys="Chore.creator_id",
					back_populates="creator")
	assigned_chores = db.relationship("Chore", foreign_keys="Chore.assignee_id",
					back_populates="assignee")

class Chore(db.Model):
	__tablename__ = "chores"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	due_date = db.Column(db.Date, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)



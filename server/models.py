from config import db, bcrypt
from datetime import datetime, date

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	password_hash = db.Column(db.String, nullable=False)

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

	completion = db.relationship("Complete", back_populates="chore",
							uselist=False)

	creator = db.relationship("User", foreign_keys=[creator_id], back_populates="created_chores")
	assignee = db.relationship("User", foreign_keys=[assignee_id], back_populates="assigned_chores")

	def to_dict(self):
		if self.completion:
			completed_on = self.completion.completed_on.isoformat()
		else:
			completed_on = None


		if self.completion:
			status = "completed"
		elif self.due_date < date.today():
			status = "overdue"
		else:
			status = "pending"

		return {
			"id": self.id,
			"title": self.title,
			"status": status,
			"due_date": self.due_date.isoformat(),
			"creator": self.creator.username,
			"assignee": self.assignee.username,
			"completed_on": completed_on
		}




class Complete(db.Model):
	__tablename__ = "completed"

	id = db.Column(db.Integer, primary_key=True)
	chore_id = db.Column(db.Integer, db.ForeignKey("chores.id"),
				unique=True, nullable=False)

	completed_on = db.Column(db.DateTime, nullable=False)

	chore = db.relationship("Chore", back_populates="completion")

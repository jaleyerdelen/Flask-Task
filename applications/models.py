from applications import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)

    def __repr__(self):
        return f"Item {self.name}"

class Photo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
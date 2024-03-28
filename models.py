"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    image_url = db.Column(db.String(200),
                          nullable=False)
    def __repr__(self):
        return f"<User id={self.id} First Name={self.first_name} Last Name={self.last_name} Image URL={self.image_url}>"
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
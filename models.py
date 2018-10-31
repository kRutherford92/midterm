# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# create new instance
db = SQLAlchemy()

# Create class User
class Users(db.Model):
	_tablename_ = 'users'
	uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)

# Create class Condo
class Condos(db.Model):
	__tablename__ = 'condos'
	cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	mlsnum = db.Column(db.Integer, nullable=False)
	display_x = db.Column(db.Float, nullable=False)
	display_y = db.Column(db.Float, nullable=False)
	beds = db.Column(db.Integer, nullable=False)
	baths = db.Column(db.Float, nullable=False)
	sqft = db.Column(db.Integer, nullable=False)
	ppsf = db.Column(db.Float, nullable=False)
	photo_url = db.Column(db.String(64), nullable=False)
	list_price = db.Column(db.Integer, nullable=False)
	predicted_price = db.Column(db.Float, nullable=False)
	remarks = db.Column(db.String(1000), nullable=False)

# Create class Like
class Likes(db.Model):
	__tablename__ = 'likes'
	lid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	liker = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
	liked = db.Column(db.Integer, db.ForeignKey('condos.cid'), nullable=False)
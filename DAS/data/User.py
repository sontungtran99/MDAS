from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = 'users'
	phonenum = db.Column(db.String(15), unique=True, nullable=False, primary_key=True)
	district = db.Column(db.String(30), nullable=False)
	province = db.Column(db.String(30), nullable=False)

	def __repr__(self):
		return '<User {} in dist. {}, province {}'.format(self.phonenum, self.district, self.province)
	



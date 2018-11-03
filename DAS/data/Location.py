from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vietnamLoc.db'
db_locations = SQLAlchemy(app)

class Location(db_locations.Model):
	__tablename__ = 'vietnamLoc'
	id = db_locations.Column(db_locations.Integer, primary_key=True)
	district = db_locations.Column(db_locations.String(30), nullable=False)
	province = db_locations.Column(db_locations.String(30), nullable=False)

	def __repr__(self):
		try:
			return '<Location {} dist., {} prov.>'.format(self.district, self.province)
		except Exception:
			return 'None'

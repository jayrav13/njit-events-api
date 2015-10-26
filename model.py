# Imports
# flask
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# sqlalchemy
from sqlalchemy import Integer, ForeignKey, String, Column, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

# other
import time
import hashlib

# set up app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///events.db" 

# set up database
db = SQLAlchemy(app)

# set up migration
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('events', MigrateCommand)

class Events(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	summary = db.Column(db.String)
	location = db.Column(db.String)
	dtstart = db.Column(db.String)
	dtend = db.Column(db.String)
	all_day = db.Column(db.String)
	organization = db.Column(db.String)
	description = db.Column(db.String)
	category = db.Column(db.String)
	
	def __init__(self, name, summary, location, dtstart, dtend, all_day, organization, description, category):
		self.name = name
		self.summary = summary
		self.location = location 
		self.dtstart = dtstart
		self.dtend = dtend
		self.all_day = all_day
		self.organization = organization
		self.description = description
		self.category = category 
		
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String)
	password = db.Column(db.String)
	token = db.Column(db.String)

	def __init__(self, email, password):
		self.email = email
		self.password = hashlib.md5(password).hexdigest()
		self.token = hashlib.md5(email + ":" + str(time.time()) + ":" + password).hexdigest()

if __name__ == "__main__":
	manager.run()

# Imports
# flask
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# sqlalchemy
from sqlalchemy import Integer, ForeignKey, String, Column, Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

# other
import time
import hashlib

# keys
import secret

# set up app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = secret.DB_KEY 

# set up database
db = SQLAlchemy(app)

# set up migration
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('events', MigrateCommand)

class Events(db.Model):

	__tablename__ = "eventsv2"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	summary = db.Column(db.Text)
	location = db.Column(db.Text)
	dtstart = db.Column(db.Text)
	dtend = db.Column(db.Text)
	all_day = db.Column(db.Text)
	organization = db.Column(db.Text)
	description = db.Column(db.Text)
	category = db.Column(db.Text)
	
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

	__tablename__ = "usersv2"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.Text)
	password = db.Column(db.Text)
	token = db.Column(db.Text)

	def __init__(self, email, password):
		self.email = email
		self.password = hashlib.md5(password).hexdigest()
		self.token = hashlib.md5(email + ":" + str(time.time()) + ":" + password).hexdigest()

class Analysis(db.Model):

	__tablename__ = "analysisv2"

	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.Text)
	loadtime = db.Column(db.Text)
	uid = db.Column(db.Text)
	device = db.Column(db.Text)
	ip = db.Column(db.Text)

	def __init__(self, datetime, loadtime, uid, device, ip):
		self.datetime = datetime
		self.loadtime = loadtime
		self.uid = uid
		self.device = device
		self.ip = ip

if __name__ == "__main__":
	manager.run()

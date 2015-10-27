from flask import Flask, jsonify, make_response, render_template, request, session, redirect
import requests
from model import db, Events, Users
from flask.ext.assets import Environment, Bundle
import dateutil.parser
import datetime
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'My-Secret-Key'
assets = Environment(app)

css = Bundle('css/styles.css', output='gen/packed.css')
assets.register('css_all', css)

# Functions
def dt_string(time, output):
	return datetime.datetime.strftime(dateutil.parser.parse(time), output)

### login_required wrapper
### Restricts specific pages to users-only.
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		db.session.commit()
		if 'logged_in' not in session.keys():
			return redirect('/login')
		
		return f(*args, **kwargs)
	return decorated_function

# Routes
@app.route('/')
def home():
	return "Hello, world!"

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template("login.html")
	elif request.method == 'POST':
		if 'email' not in request.form or 'password' not in request.form:
			return "BAD"
		else:
			user = Users.query.filter_by(email=request.form['email']).filter_by(password=hashlib.md5(request.form['password']).hexdigest()).first()
			
			if user:
				session['logged_in'] = user.id
				return redirect('/user')
			else:
				return "BAD LOGIN"

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template("register.html", title="Register")
	elif request.method == 'POST':
		if 'email' not in request.form or 'password' not in request.form:	
			return make_response(jsonify({'error':'Required fields not sent.'}), 400)
		else:
			user = Users.query.filter_by(email=request.form['email']).first()

			if user:
				return make_respose(jsonify({'error':'User already exists.'}), 409)
			else:
				user = Users(request.form['email'], request.form['password'])	
				db.session.add(user)
				db.session.commit()
				return make_response(jsonify({'success':user.token}), 200)

@app.route('/api/v0.2/events', methods=['GET'])
def events():
	events = Events.query.all()
	arr = []
	currentdate = datetime.datetime.now()

	for event in events:

		if currentdate < dateutil.parser.parse(event.dtend):
			dict = {
				'id' : event.id,
				'name' : event.name,
				'summary' : event.summary,
				'location' : event.location,
				'organization' : event.organization,
				'category' : event.category,
				'description' : event.description,
				'datetime' : {
					'is_today' : currentdate.date() == dateutil.parser.parse(event.dtstart).date(),
					'is_tomorrow' : currentdate.date() + datetime.timedelta(days=1) == dateutil.parser.parse(event.dtstart).date(),
					'currently_happening' : currentdate > dateutil.parser.parse(event.dtstart),
					'all_day' : event.all_day == "TRUE",
					'time_range_string' : dt_string(event.dtstart, '%I:%M %p') + " - " + dt_string(event.dtend, '%I:%M %p'),
					'multiday' : dateutil.parser.parse(event.dtstart).date() != dateutil.parser.parse(event.dtend).date(),
					'start' : {
						'dtstart' : event.dtstart,
						'common_formats' : {
							'date' : dt_string(event.dtstart, '%m/%d/%Y'),
							'time' : dt_string(event.dtstart, '%I:%M %p')
						}
					}, 
					'end' : {
						'dtend' : event.dtend,
						'common_formats' : {
							'date' : dt_string(event.dtend, '%m/%d/%Y'),
							'time' : dt_string(event.dtend, '%I:%M %p')
						}
					} 
				}
			}
			arr.append(dict)

	return make_response(jsonify({'response' : arr}), 200)

	
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# create instance of flask web application
app = Flask(__name__)
app.secret_key = 'hello'
# users here is the name of the table that will be referenced
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# this flag to ignore some warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# example of changing permanent session lifetime, default is 30 days
app.permanent_session_lifetime = timedelta(minutes=5)

# sets up new sql database object
db = SQLAlchemy( app )

# user object - extends db.Model
class users( db.Model ):
	# primary key meaning a guaranteed unique identifier
	_id = db.Column( 'id', db.Integer, primary_key=True )
	# if the first param is not provided to db.Column it will default to the python var name
	name = db.Column( 'name', db.String(100) )
	email = db.Column( 'email', db.String(100) )

	def __init__( self, name, email ):
		# when the primary key is not provided here it will be auto generated
		self.name = name
		self.email = email

# function decorator for defining where this function is shown
@app.route('/')
def home():
    return render_template('index.html')

# view entire database
@app.route('/view')
def view():
	return render_template('view.html', values=users.query.all())

# methods param used to specify which requests will be used
@app.route('/login', methods=['POST', 'GET'])
def login():
	# user provides name
	if request.method == 'POST':
		session.permanent = True
		user = request.form['nm']
		# username stored as session data
		session['user'] = user

		# query users table for column with name equal to name from form
		found_user = users.query.filter_by(name=user).first()
		# deletion syntax
		# users.query.filter_by(name=user).delete()
		if found_user:
			session['email'] = found_user.email
		else:
			usr = users( user, '' )
			# adds to "staging" area
			db.session.add(usr)
			# commits to database
			db.session.commit()

		flash('Login Succesful')
		return redirect(url_for('user'))
	# user requests login page
	else: 
		if 'user' in session:
			flash('Already Logged In')
			return redirect(url_for('user'))
			
		return render_template('login.html')

# user page has static route but can only be accessed if user is 
# logged in which is verified by session data
@app.route('/user', methods=['POST', 'GET'])
def user():
	email = None
	# if user is logged in
	if 'user' in session:
		user = session['user']
		
		# POST - user is providing their email
		if request.method == 'POST':
			email = request.form['email']
			session['email'] = email

			# query users table for column with name equal to name from form
			found_user = users.query.filter_by(name=user).first()
			found_user.email = email
			db.session.commit()

			flash('Email was saved!')
		# GET - user is requesting to see their email
		else:
			if 'email' in session:
				email = session['email']

		return render_template('user.html', email=email)
	else:
		flash('You are not logged in!')
		return redirect(url_for('login'))

# clearing session data 'user' effectively logs user out via flow of pages
@app.route('/logout')
def logout():
	if 'user' in session:
		user = session['user']
		# notifcation type message - shows up on next page
		flash(f'You have been logged out, {user}!', 'info')
	session.pop('user', None)
	session.pop('email', None)
	return redirect(url_for('login'))

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)

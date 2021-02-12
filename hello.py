from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
# create instance of flask web application
app = Flask(__name__)
app.secret_key = 'hello'
# example of changing permanent session lifetime, default is 30 days
app.permanent_session_lifetime = timedelta(minutes=5)

# function decorator for defining where this function is shown
@app.route('/')
def home():
    return render_template('index.html')

# methods param used to specify which requests will be used
@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		session.permanent = True
		user = request.form['nm']
		# username stored as session data
		session['user'] = user
		flash('Login Succesful')
		return redirect(url_for('user'))
	else: 
		if 'user' in session:
			flash('Already Logged In')
			return redirect(url_for('user'))
			
		return render_template('login.html')

# user page has static route but can only be accessed if user is 
# logged in which is verified by session data
@app.route('/user')
def user():
	if 'user' in session:
		user = session['user']
		return render_template('user.html', user=user)
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
	return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

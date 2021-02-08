from flask import Flask, redirect, url_for, render_template, request
# create instance of flask web application
app = Flask(__name__)

# function decorator for defining where this function is shown
@app.route('/')
def home():
    return render_template('index.html')

# methods param used to specify which requests will be used
@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		user = request.form['nm']
		return redirect(url_for('user', usr=user))
	else: 
		return render_template('login.html')

# user page that should be accessed via login but is
# not currently protected
@app.route('/<usr>')
def user(usr):
	return f'<h1>{usr}</h1>'


if __name__ == '__main__':
    app.run(debug=True)

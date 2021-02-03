from flask import Flask, redirect, url_for
# create instance of flask web application
app = Flask(__name__)

# function decorator for defining where this function is shown
@app.route('/')
def home():
    return '<h1>Hello, World!</h1>'

# <name> tag passes as parameter
@app.route('/<name>')
def user(name):
    return f'Hello {name}!'

@app.route('/admin')
def admin():
    # redirects are done by function not route
    return redirect(url_for('user', name="Admin!"))

if __name__ == '__main__':
    app.run()

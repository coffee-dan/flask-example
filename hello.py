from flask import Flask, render_template
# create instance of flask web application
app = Flask(__name__)

# function decorator for defining where this function is shown
@app.route('/<name>')
def home(name):
    return render_template("index.html", content=['tim', 'joe', 'bill'])

if __name__ == '__main__':
    app.run()

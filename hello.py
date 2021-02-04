from flask import Flask, render_template
# create instance of flask web application
app = Flask(__name__)

# function decorator for defining where this function is shown
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

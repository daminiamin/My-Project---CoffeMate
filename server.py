"""Sample Flask app for SQLAlchemy homework."""

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db
from model import 

app = Flask(__name__)
app.secret_key = 'ABCSECRETDEF'


@app.route('/') #GET
def landing_page():
    """Show landing page."""

    return render_template('landing_page.html')

@app.route('/') #POST
def landing_page():
    """Log in or create user"""
    #get email, password, etc

    #if user selected log in and user exists -> return render_template('homepage.html')
    #if user selected sign up -> return render_template('sign_up.html')

@app.route('/set-up')#GET
def set_up():
    """Show set up page"""

    return render_template("set_up.html")


@app.route('/set-up')#POST
def set_up():
    """Show set up page"""

    return render_template("homepage.html")



@app.route('/profile/<string:userId>')
def profile(userId):
    """Show set up page"""

    #username = request.args.
    return render_template("profile.html")




if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

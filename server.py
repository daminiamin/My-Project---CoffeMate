"""Sample Flask app for SQLAlchemy homework."""

from jinja2 import StrictUndefined

from flask import Flask, render_template,request,flash,redirect,session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db,db,User,Hobbie,Like,Dislike,Image

app = Flask(__name__)
app.secret_key = 'ABCSECRETDEF'


@app.route('/', methods=['GET']) #GET
def landing_page():
    """Show landing page."""
    print("Not working")
    return render_template('landing_page.html')

@app.route('/login', methods=['POST']) #POST
def login():
    """ User Login """

    #if user selected log in and user exists return render_template('homepage.html')
    email = request.form["email"]
    password = request.form["password"]

    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
        if user_exists.password == password:
            session["user_id"] = user.user_id
            flash("Logged in")
            return redirect(f"/profile/{user.user_id}")
        else:
            flash("Incorrect password")
    else:
        flash("No such user")
    
    return redirect("/")


@app.route('/set-up', methods=['POST'])#POST
def set_up():
    """Show set up page"""

    # getting info of new user from singup form
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(fname= fname,lname=lname,email=email,password=password)
    
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.user_id
    flash("SingUp ")

    return render_template("set_up.html")



@app.route('/add-user', methods=['POST'])#POST
def add_user():
    # Get user from db based on session user id

    current_user = User.query.get(session["user_id"])



@app.route('/profile/<int:user_id>')
def profile(userId):
    """Show set up page"""

    #username = request.args.
    return render_template("profile.html")




if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

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
    """ User Login Page """

    #if user selected log in and user exists return render_template('homepage.html')
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user:
        if user.password == password:
            session["user_id"] = user.user_id
            flash("Logged in")
            return redirect(f"/homepage")
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
    
    user = User.query.filter_by(email=email).first()
    if user:
        # if user.password == password:
        flash(" User already exists")
        return redirect("/")

    else:
        session["fname"]=fname
        session["lname"]=lname
        session["email"]=email
        session["password"]=password

        flash("SingUp ")

        return render_template("set_up.html")

@app.route('/add-user', methods=['POST'])#POST
def add_user():
    # Get user from db based on session user id


    age = request.form["age"]
    gender = request.form["fm"]
    city = request.form["city"]
    state = request.form["state"]
    contact = request.form["contact"]
    occupation = request.form["occupation"]
    hobbie = request.form["hobbie"]  
    aboutme = request.form["aboutme"]

    new_user = User(fname=session['fname'], lname = session["lname"],
                    email= session["email"],password =session["password"],
                    age=age,gender=gender,city=city,state=state,
                    contact_no=contact,occupation=occupation,yourself=aboutme)
    
    hobbies = Hobbie(hobbie_name=hobbie, user=new_user)

    db.session.add(new_user)
    db.session.add(hobbies)
    db.session.commit()

    session["user_id"] = new_user.user_id
    flash("SingUp Successfully")
    return redirect(f"/homepage")




@app.route('/homepage')
def homepage():
    """Show  homepage page"""

    user_id = session["user_id"]
    user_info = User.query.filter_by(user_id=user_id).first()

    return render_template("homepage.html",user_info=user_info)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    """Show  profile page"""

    user_info = User.query.filter_by(user_id=user_id).first()

    return render_template("profile.html",user_info=user_info)


@app.route('/logout')
def logout():
    """logout profile page"""


    session.pop('user_id')
    return redirect("/")


    # user = SessionUser.find_by_session_id(user_id) #hits the database
    # if user is None:
    #     flash('You have been automatically logged out')
    #     session['user_id'] = None
    # return user


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

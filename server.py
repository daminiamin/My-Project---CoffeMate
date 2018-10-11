"""Sample Flask app for SQLAlchemy homework."""

from jinja2 import StrictUndefined

from flask import Flask, render_template,request,flash,redirect,session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db,db,User,Hobbie,User_Hobbies,Like,Dislike,Image

app = Flask(__name__)
app.secret_key = 'ABCSECRETDEF'


@app.route('/', methods=['GET']) #GET
def landing_page():
    """Show landing page."""
    return render_template('landing_page.html')

@app.route('/login', methods=['POST']) #POST
def login():
    """ User Login Page """

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
    #if user selected log in and user exists return render_template('homepage.html')

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

        hobbies_info = Hobbie.query.all()
        # query the database to get all hobbie objects from the Hobbie table
        return render_template("set_up.html",hobbies_info=hobbies_info)
        # pass that list of hobbie objects into render_template for the setup html page)


@app.route('/add-user', methods=['POST'])#POST
def add_user():
    # Get user from db based on session user id

    age = request.form["age"]
    gender = request.form["gender"]
    city = request.form["city"]
    state = request.form["state"]
    contact = request.form["contact"]
    occupation = request.form["occupation"]
    hobbies = request.form.getlist("hobbie") 
        #getting list of hobbies from user 
    aboutme = request.form["aboutme"]

    new_user = User(fname=session['fname'], lname = session["lname"],
                    email= session["email"],password =session["password"],
                    age=int(age),gender=gender,city=city,state=state,
                    contact_no=contact,occupation=occupation,yourself=aboutme)
    
    db.session.add(new_user)

    for hobbie in hobbies:
        new_hobbie = User_Hobbies(hobbie_id=int(hobbie), user=new_user)
        db.session.add(new_hobbie)
        #adding every hobbie which user selected and adding to db
    
    db.session.commit()

    session["user_id"] = new_user.user_id
    flash("SingUp Successfully")
    return redirect(f"/homepage")


@app.route('/homepage')
def homepage():
    """Show  homepage page"""

    user_id = session["user_id"]
    user_info = User.query.get(user_id)

    get_likes = user_info.likes # list of all users that the current user likes.
    likes_ids = set([like.user_id for like in get_likes])
    #get likes user,liked by current user

    get_dislikes = user_info.dislikes
    dislikes_ids = set([dislike.user_id for dislike in get_likes])
    #get dislikes user,liked by current user

    print(likes_ids)
    print(dislikes_ids)

    all_users = User.query.all()
    set_users = set([user.user_id for user in all_users ])

    # likes_dislikes = list(set(get_likes + get_dislikes))

    suggestions = (set_users - ((likes_ids) + (dislikes_ids)) - set(user_id))

 
    # get_suggestions = []

    # if total:
    #     if total in set_users:
    #         set_users.pop(total)
    #     else:
    #         get_suggestions.append(set_users)

    # # get_three
    # make set of all user_id's
    # make set of all ids in get_likes
    # make set of all ids in get_dislikes
    # set of user_id's - (set of ids in likes + set of ids in dislikes)
    # pick 3 from that

    #remove users they like/dislike
    #get3 users who has same hobbie
        #1,3,3,4 remove users
    #make another query to store both queries varibale

    return render_template("homepage.html", user_info=user_info,
                                            suggestions=suggestions)


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

"""Sample Flask app for SQLAlchemy homework."""

from jinja2 import StrictUndefined

from flask import Flask, render_template,request,flash,redirect,session
from flask_debugtoolbar import DebugToolbarExtension
from random import sample
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
    interested_in = request.form["interested_in"]
    city = request.form["city"]
    state = request.form["state"]
    contact = request.form["contact"]
    occupation = request.form["occupation"]
    hobbies = request.form.getlist("hobbie") 
        #getting list of hobbies from user 
    aboutme = request.form["aboutme"]

    new_user = User(fname=session['fname'], lname = session["lname"],
                    email= session["email"],password =session["password"],
                    age=int(age),gender=gender,interested_in=interested_in,
                    city=city,state=state,contact_no=contact,
                    occupation=occupation,yourself=aboutme)
    
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
    # print(f"user_info {user_info}")

    get_likes = user_info.likes # list of all users that the current user likes.
    liked_ids = set([like.liked_user_id for like in get_likes])
    #get likes user,liked by current user

    get_dislikes = user_info.dislikes
    disliked_ids = set([dislike.disliked_user_id for dislike in get_dislikes])
    #get dislikes user,liked by current user

    excluded_ids = (liked_ids) | (disliked_ids) | set([user_id])
    # adding likes_dislikes of current user

    # suggestions = (interesting_user_ids - likes_dislikes) - set([user_id])
    # substracting likes/dislikes,current user ids with same gender people
    # print(f"suggestions {suggestions}")

    # build a list of hobbie ids for current user
    current_user_hobbies = [hobbie.hobbie_id for hobbie in user_info.hobbies]

    # join with user hobbies and select only users where the hobbies in list
    all_interest_users = User.query.join(User_Hobbies).filter((User.gender == user_info.interested_in),
                                User_Hobbies.hobbie_id.in_(current_user_hobbies),
                                User.user_id.notin_(list(excluded_ids))).all()

    #macthing interested_in of current user 
                # to show all users who is that gender only
                    #get users with cross  M/F connections

    # interesting_user_ids = set([user.user_id for user in all_interest_users ])
    # store all user id's of that all same gender users


    # get_allobjects = db.session.query(User).filter(User.user_id.in_(suggestions)).all()
    # getting all users object using all suggestion id
    

    # get current user's hobbies
    # get_same_hobbie_users=db.session.query(User).filter(User.hobbie_id.in_(current_user_hobbies)).all()
    # getting users who has same hobbie as current user



    if len(all_interest_users) > 3:

        all_interest_users = sample(all_interest_users, 3)
        #get3 users who has same hobbie


    # if button like:
    #     user.add.current user
    # elif dislikes:
    #     user.add.c

    #user clicks on heart it should added into her/his list
    #user clicks on dislikes  it should remove that person from suggestion temparary

    return render_template("homepage.html", user_info=user_info,
                                            get_allobjects=all_interest_users)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    """Show the user profile for that user."""

    user_info = User.query.get(user_id)

    # user_info = User.query.filter_by(user_id=user_id).first()

    return render_template("profile.html", user_info=user_info)


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


@app.route('/like')
def like():
    """ liking user by saving into database """

    user_id = session["user_id"]

    liked = request.form['liked']

    liked_user = Like(likes_user_id=int(user_id),liked_user_id =int(liked))
    
    db.session.add(liked_user)
    db.session.commit()

    return redirect("/homepage")


@app.route('/dislike')
def dislike():
    """ disliking user by saving into database """



    user_id = session["user_id"]

    disliked = request.form['disliked']

    disliked_user = Dislike(dislikes_user_id=int(user_id),disliked_user_id =int(disliked))
    
    db.session.add(disliked_user)
    db.session.commit()

    return redirect("/homepage")




##########Test Route##################

# @app.route('/test')
# def test():

#     return render_template("test.html")
##########################

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

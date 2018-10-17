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
    user_info = User.query.get(user_id) #current user info
    # print(f"user_info {user_info}")

    get_likes = user_info.likes #list of all users liked by current user.
    liked_ids = set([like.liked_user_id for like in get_likes])

    get_dislikes = user_info.dislikes #list of all users disliked by current user.
    disliked_ids = set([dislike.disliked_user_id for dislike in get_dislikes])
    
    # adding likes_dislikes of current user 
    excluded_ids = (liked_ids) | (disliked_ids) | set([user_id])

    # build a list of hobbie ids for current user
    current_user_hobbies = [hobbie.hobbie_id for hobbie in user_info.hobbies]

    # join with user hobbies and select only users where the hobbies in list
    all_interest_users = User.query.join(User_Hobbies).filter((User.gender == user_info.interested_in),
                                User_Hobbies.hobbie_id.in_(current_user_hobbies),
                                User.user_id.notin_(list(excluded_ids))).all()
    #macthing interested_in current user 
                # show all users who has common hobbies 
                    #get users not in excluded_ids(likes,dislikes,c.Uid)


    if len(all_interest_users) > 3:

        all_interest_users = sample(all_interest_users, 3)
        #get3 users who has same hobbie

    return render_template("homepage.html", user_info=user_info,
                                            get_allobjects=all_interest_users)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    """Show the user profile for that user."""

    another_user_info = User.query.get(user_id)

    # user_info = User.query.filter_by(user_id=user_id).first()

    return render_template("profile.html", user_info=another_user_info)


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

############## LIKE ############################
@app.route('/like', methods=['POST'])
def like():
    """ liking user by saving into database """

    user_id = session["user_id"]#current user id

    liked_user_id = int(request.form.get('likedUserId'))#liked user id

    # query Like table to see if this user has already liked the person
    liked_in_like = Like.query.filter_by(likes_user_id=user_id , liked_user_id=liked_user_id).first()

    if not liked_in_like:
        # adding liked user to like table
        add_liked_user = Like(likes_user_id=user_id,liked_user_id=liked_user_id)
        db.session.add(add_liked_user)

    # check liked user exist in dislike table DB
    liked_in_dislike = Dislike.query.filter_by(dislikes_user_id=user_id , disliked_user_id=liked_user_id).first()

    if liked_in_dislike:
        # delete record from dislike table
        db.session.delete(liked_in_dislike)
    
    db.session.commit()

    return "OK"
############## UNLIKE ############################

@app.route('/unlike', methods=['POST'])
def unlike():
    """ unliking user by saving into database """

    user_id = session["user_id"]#current user id

    unliked_user_id = int(request.form.get('likedUserId'))#unliked user id

    # check if unliked user in like tbl
    unliked_in_like =Like.query.filter_by(likes_user_id=user_id, liked_user_id=unliked_user_id).first()

    
    if unliked_in_like:
        # delete record from Dislike table
        db.session.delete(unliked_in_like)

    db.session.commit()
    return "OK"

############## DISLIKE ############################

@app.route('/dislike', methods=["POST"])
def dislike():
    """ disliking user by saving into database """

    user_id = session["user_id"]#current user id

    disliked_user_id = int(request.form.get('dislikedUserId')) 

    # Check to see if this user already dislikes the person
    disliked_in_dislike = Dislike.query.filter_by(dislikes_user_id=user_id , disliked_user_id=disliked_user_id).first()

    if not disliked_in_dislike:
        # adding disliked user to Dislike table
        add_disliked_user = Dislike(dislikes_user_id=user_id,disliked_user_id=disliked_user_id)
        db.session.add(add_disliked_user)

    # check disliked user in likes tbl
    disliked_in_like = Like.query.filter_by(likes_user_id=user_id, liked_user_id=disliked_user_id).first()

    if disliked_in_like:
        # delete record from like table
        db.session.delete(disliked_in_like)

    db.session.commit()
    return "OK"

############## UNDISLIKE ############################

@app.route('/undislike', methods=['POST'])
def undislike():
    """ undisliking user by saving into database """

    user_id = session["user_id"]#current user id

    undisliked_user_id = int(request.form.get('dislikedUserId'))#undisliked user id

    # check if disliked user in dislike tbl
    undisliked_in_dislike = Dislike.query.filter_by(dislikes_user_id=user_id,disliked_user_id=undisliked_user_id).first()
 
    if undisliked_in_dislike:
        # delete record from Dislike table
        db.session.delete(undisliked_in_dislike)

    db.session.commit()
    return "OK"

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

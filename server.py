from geopy.geocoders import Nominatim #for long-lat
from geopy import distance
import requests #for api req
import hashlib
from pprint import pprint
import os
from jinja2 import StrictUndefined
import json
from flask import Flask, render_template,jsonify,request,flash,redirect,session,url_for
from flask_debugtoolbar import DebugToolbarExtension
from random import sample
from werkzeug.utils import secure_filename
from model import connect_to_db,db,User,Hobbie,User_Hobbies,Like,Dislike,Image

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


#######Google Stuff ########
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
######################## Creating/Sending Email ###########################################

import base64
from email.mime.text import MIMEText

###############################################################

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'uc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
yelp_api_key = os.environ['YELP_KEY']   #Yelp key 
yelp_url = "https://api.yelp.com/v3/businesses" #yelp url

################################################################################


# stores a file that contains the OAuth 2.0 information including its 
# client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secrets.json"

SCOPES = ['https://mail.google.com/']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def create_message(to, subject, message_text):
    """Create a message for an email.
    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    message_bytes = message.as_bytes() # turn MIMETEXT into byte string
    # encode byte string to base64 encoding and then decode the result into a regular string
    result = {'raw': base64.urlsafe_b64encode(message_bytes).decode()}
    print(result)
    return result


def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print("Message Id: %s" % message['id'])
        return message

    except googleapiclient.errors.HttpError as error:
        print("An error occurred: %s" % error)
        return error


@app.route('/send_email')
def send_email():
    """ This is the route that should accept data from an email form"""
    # message = request.args.get('message')

    recipient =request.args["recipient-email"]
    subject = request.args["subject"]
    message = request.args["message"]
    

    # If user is not authorized...
    if 'credentials' not in session:
        return "Please authorize first on homepage"

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    gmail = googleapiclient.discovery.build(
                        API_SERVICE_NAME, API_VERSION, credentials=credentials)
                        # call version 1 of the gmail API:

    session['credentials'] = credentials_to_dict(credentials)

    email = create_message(recipient, subject, message)
    result = send_message(gmail, "me", email)

    return "Email sent"
################################################################################

@app.route('/authorize')
def authorize():
    if 'credentials' in session:
        return redirect('/homepage')

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state
    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    flash("User authorized")
    return redirect('/homepage')

def credentials_to_dict(credentials):
    return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


@app.route('/revoke')
def revoke():
  if 'credentials' not in session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **session['credentials'])

  revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.')
  else:
    return('An error occurred.' )


@app.route('/clear')
def clear_credentials():
  if 'credentials' in session:
    del session['credentials']
  return ('Credentials have been cleared.<br><br>')
# ÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷ My Routes ÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷÷



@app.route('/')
def main():
    """Show Main page."""
    return render_template("main.html")



@app.route('/login')
def login_page():
    """Show login page."""
    return render_template('login.html')


@app.route('/login', methods=['POST']) 
def login():
    """ User Login Page """

    email = request.form["email"]
    password = request.form["password"]
    password = password.encode() #byte code convert paswd
    hash_pwd = hashlib.sha256(password)
    hash_pwd = hash_pwd.hexdigest()

    user = User.query.filter_by(email=email).first()

    if user:
        if user.password == hash_pwd:
            session["user_id"] = user.user_id
            flash("Logged in")
            return redirect(f"/homepage")
        else:
            flash("Incorrect password")
    else:
        flash("No such user")

    return redirect("/login")


@app.route('/signup')
def signup():
    """Show signup page."""
    
    return render_template("signup.html")


@app.route('/set-up', methods=['POST'])
def set_up():
    """Show set up page"""

    # getting info of new user from signup form
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]
    password = password.encode() #byte code convert paswd
    hash_pwd = hashlib.sha256(password)
    hash_pwd = hash_pwd.hexdigest()
    
    user = User.query.filter_by(email=email).first()
    if user:
        # if user.password == password:
        flash(" User already exists")
        return redirect("/signup")

    else:
        session["fname"]=fname
        session["lname"]=lname
        session["email"]=email
        session["password"]=hash_pwd

        flash("create you profile ")

        # query the database to get all hobbie objects from the Hobbie table
        hobbies_info = Hobbie.query.all()

        # pass that list of hobbie objects into render_template for the setup html page)
        return render_template("set_up.html",hobbies_info=hobbies_info)

# upload file function
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add-user', methods=['POST']) #POST from setup page
def add_user():
    """ add new user's information """

    age = request.form["age"]
    gender = request.form["gender"]
    interested_in = request.form["interested_in"]
    city = request.form["city"]
    state = request.form["state"]
    state = state.upper()
    contact = request.form["contact"]
    occupation = request.form["occupation"]
            #getting list of hobbies from user 
    hobbies = request.form.getlist("hobbie") 
    aboutme = request.form["aboutme"]
    # upload profile picture
    file = request.files["file"]

                    # Get user info from session 
    new_user = User(fname=session['fname'], lname = session["lname"],
                    email= session["email"],password =session["password"],
                    age=int(age),gender=gender,interested_in=interested_in,
                    city=city,state=state,contact_no=contact,
                    occupation=occupation,yourself=aboutme)
    
    db.session.add(new_user)
    db.session.commit()

    for hobbie in hobbies:
        #adding every hobbie which user selected and adding to user_hobbies table
        new_hobbie = User_Hobbies(hobbie_id=int(hobbie), user=new_user)
        db.session.add(new_hobbie)
    db.session.commit()

    if file.filename == "":
        flash('No selected file')
        return redirect('/add-user')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
                    # saving image with unique name in static\uploads folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                    str(new_user.user_id)+'_'+filename))

    file.filename = str(new_user.user_id)+'_'+filename
    # add image to database
    add_profile_pic = Image(user=new_user, filename=file.filename)
    db.session.add(add_profile_pic)
    db.session.commit()

    # Make this image the user's profile pic
    new_user.profile = add_profile_pic                 

    db.session.commit()

    session["user_id"] = new_user.user_id

    flash("SignUp Successfully")
    return redirect(f"/homepage")


@app.route('/homepage')
def homepage():
    """Show  user's homepage page"""

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
    all_interest_users = User.query.join(User_Hobbies).filter(
                                (User.gender == user_info.interested_in),
                                User_Hobbies.hobbie_id.in_(current_user_hobbies),
                                User.user_id.notin_(list(excluded_ids))).all()
    # print(all_interest_users)
    #macthing interested_in current user 
                # show all users who has common hobbies 
                    #get users not in excluded_ids(likes,dislikes,c.Uid)


    if len(all_interest_users) > 3:
        #get3 users who has same hobbie

        all_interest_users = sample(all_interest_users, 3)

    return render_template("homepage.html", user_info=user_info,
                                            get_allobjects=all_interest_users)


#defining function for API call
#helper function

def yelp_api(coordinates):

    headers = {'Authorization': 'Bearer '+ yelp_api_key}
    payload = {'latitude': coordinates[0],
               'longitude': coordinates[1],
               'term': 'Coffee Shop', 
               'limit': 5}
    response = requests.get(yelp_url+"/search",
                                    params=payload,
                                    headers=headers)
    
    data = response.json()

    return data


@app.route('/profile/<int:user_id>')
def profile(user_id):
    """Show another user's profile page"""

    c_user_id = session["user_id"] #current user info

    c_user_info = User.query.get(c_user_id)
    another_user_info = User.query.get(user_id)
    # checking user in like
    liked_in_like = Like.query.filter_by(likes_user_id=c_user_id , liked_user_id=user_id).first()
    # checking user in dislike
    disliked_in_dislike = Dislike.query.filter_by(dislikes_user_id=c_user_id , 
                                                disliked_user_id=user_id).first()
    
    # checking user liked back
    liked_back = Like.query.filter_by(likes_user_id=user_id,liked_user_id=c_user_id).first()

    # if current user liked this user
    if liked_in_like:
        status = 'liked'
    elif disliked_in_dislike:
        status = 'disliked'
    else:
        status = None
   
    # if that user liked back to the current user
    if liked_back and liked_in_like:
        matched = True
    else:
        matched = False


    c_user_city = c_user_info.city #current user's city
    another_user_city = another_user_info.city # another user's city
    
    geolocator = Nominatim(user_agent="")

    c_location = geolocator.geocode(c_user_city)   # saves like this ->
        #('Palo Alto, Santa Clara County, California, USA', (37.4455862, -122.1619289))
    another_location = geolocator.geocode(another_user_city)

    # Calculate the midpoint
    mid_lat = (c_location.latitude + another_location.latitude) / 2
    mid_lng = (c_location.longitude + another_location.longitude) / 2
    midpoint = (mid_lat, mid_lng) 

    # import pdb; pdb.set_trace()

    #find distance of users
    distance_of_users = distance.distance(c_location.point, another_location.point).miles

    if distance_of_users > 50:
        yelp_suggestions = []
    # Make a request to Yelp API with the midpoint coordinates
    else:
        yelp_suggestions = yelp_api(midpoint)


    return render_template("profile.html", user_info=another_user_info, 
                                            status = status, matched = matched,
                                            yelp_suggestions=yelp_suggestions)
@app.route('/logout')
def logout():
    """logout page"""


    session.pop('user_id')
    if 'credentials' in session:
        del session['credentials']
    return redirect("/")

############## LIKE ############################
@app.route('/like', methods=['POST'])
def like():
    """ liking user and saving into database """

    user_id = session["user_id"]#current user id

    liked_user_id = int(request.form.get('likedUserId'))#liked user id

    # query Like table to see if this user has already liked the person
    liked_in_like = Like.query.filter_by(likes_user_id=user_id , 
                                            liked_user_id=liked_user_id).first()

    if not liked_in_like:
        # adding liked user to like table
        add_liked_user = Like(likes_user_id=user_id,liked_user_id=liked_user_id)
        db.session.add(add_liked_user)

    # check liked user exist in dislike table DB
    liked_in_dislike = Dislike.query.filter_by(dislikes_user_id=user_id , 
                                        disliked_user_id=liked_user_id).first()

    if liked_in_dislike:
        # delete record from dislike table
        db.session.delete(liked_in_dislike)
    
    db.session.commit()

    liked_back = Like.query.filter_by(likes_user_id=liked_user_id,liked_user_id=user_id).first()
    if liked_back:
        liked_back = True
    else:
        liked_back = False

    # Query User table by liked_user_id to get phone number
    phone = db.session.query(User.contact_no).filter_by(user_id = liked_user_id).first()

    return jsonify({'status': 'ok', 'liked_back': liked_back, 'phone_num': phone})


############## UNLIKE ############################
@app.route('/unlike', methods=['POST'])
def unlike():
    """ unliking user and saving into database """

    user_id = session["user_id"]#current user id

    unliked_user_id = int(request.form.get('likedUserId'))#unliked user id

    # check if unliked user in like tbl
    unliked_in_like =Like.query.filter_by(likes_user_id=user_id, 
                                            liked_user_id=unliked_user_id).first()

    
    if unliked_in_like:
        # delete record from Dislike table
        db.session.delete(unliked_in_like)

    db.session.commit()
    return "OK"

############## DISLIKE ############################ 

@app.route('/dislike', methods=["POST"])
def dislike():
    """ disliking user and saving into database """

    user_id = session["user_id"]#current user id

    disliked_user_id = int(request.form.get('dislikedUserId')) 

    # Check to see if this user already dislikes the person
    disliked_in_dislike = Dislike.query.filter_by(dislikes_user_id=user_id , 
                                    disliked_user_id=disliked_user_id).first()

    if not disliked_in_dislike:
        # adding disliked user to Dislike table
        add_disliked_user = Dislike(dislikes_user_id=user_id,disliked_user_id=disliked_user_id)
        db.session.add(add_disliked_user)

    # check disliked user in likes tbl
    disliked_in_like = Like.query.filter_by(likes_user_id=user_id, 
                                        liked_user_id=disliked_user_id).first()

    if disliked_in_like:
        # delete record from like table
        db.session.delete(disliked_in_like)

    db.session.commit()
    return "OK"

############## UNDISLIKE ############################
@app.route('/undislike', methods=['POST'])
def undislike():
    """ undisliking user and saving into database """

    user_id = session["user_id"]#current user id

    undisliked_user_id = int(request.form.get('dislikedUserId'))#undisliked user id

    # check if disliked user in dislike tbl
    undisliked_in_dislike = Dislike.query.filter_by(dislikes_user_id=user_id,disliked_user_id=undisliked_user_id).first()
 
    if undisliked_in_dislike:
        # delete record from Dislike table
        db.session.delete(undisliked_in_dislike)

    db.session.commit()
    return "OK"

@app.route('/connections',methods=['GET'])
def connections():
    """ Show connections of user"""
    c_user_id = session["user_id"]

    c_user_info = User.query.get(c_user_id) #current user info


    get_likes = c_user_info.likes #list of all users liked by current user.
    # for loop to get only ids from objects
    liked_ids = set([like.liked_user_id for like in get_likes])
    
    liked_back = db.session.query(User).join(Like.likes_user).filter(Like.likes_user_id.in_(liked_ids),Like.liked_user_id==c_user_id).all()

    


    return render_template("connections.html",liked_back=liked_back)


@app.route('/change-info',methods=['GET'])
def change_info():
    """ allow user to change info of a user """
     

@app.route('/change-profile',methods=['GET'])
def change_profile():
    """ allow user to change profile image """


@app.route('/delete-account',methods=['GET'])
def delete_account():
    """ delete account"""


##########Test Route##################


##########################

if __name__ == "__main__":
    # app.debug = False
    app.debug = True

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

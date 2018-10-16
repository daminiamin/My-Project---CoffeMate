"""Models and database functions for Dating Project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
    # Model definitions


class User(db.Model):
    """User of dating website."""

    __tablename__ = "users"


    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fname   = db.Column(db.String(25), nullable = False)
    lname   = db.Column(db.String(25), nullable = False)
    email   = db.Column(db.String(100), nullable = False)
    password= db.Column(db.String(25), nullable= False)
    age     = db.Column(db.Integer, nullable = False)
    gender= db.Column(db.String(1), nullable = False)
    interested_in = db.Column(db.String(1), nullable = False)
    city    = db.Column(db.String(25), nullable = False)
    state =db.Column(db.String(25), nullable = False)
    contact_no = db.Column(db.String(10), nullable = False)
    occupation = db.Column(db.String(25), nullable=False)
    yourself = db.Column(db.String(200), nullable=True)

    ######### Define Relationship ############

    hobbies = db.relationship('Hobbie', secondary="user_hobbies", backref="users")

    # likes = db.relationship('Like', foreign_keys='likes_user_id')
    # likers = db.relationship('Like', foreign_keys='liked_user_id')    
    # dislikes = db.relationship('Dislike', foreign_keys='dislikes_user_id')
    # dislikers = db.relationship('Dislike', foreign_keys='disliked_user_id')

    images = db.relationship('Image')

    def __repr__(self):

        """ Provide helpful representation when printed """
        us = f"""< User user_id = {self.user_id} 
                        fname = {self.fname}
                        lname = {self.lname}
                        email = {self.email}
                        password = {self.password}
                        age = {self.age}
                        gender = {self.gender}
                        interested_in = {self.interested_in}
                        city={self.city}
                        state={self.state}
                        contact_no={self.contact_no}>"""
        return us

class Hobbie(db.Model):
    """Hobbie model of dating website"""

    __tablename__ = "hobbies"

    hobbie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    hobbie_name = db.Column(db.String(25),unique=True, nullable=False)
    #relationship
    # user = db.relationship('User')

    def __repr__(self):

        """ Provide helpful representation when printed """
        hb = f"""<Hobbie    hobbie_id ={self.hobbie_id}
                    
                            hobbie_name={self.hobbie_name}>"""
                        #user_id ={self.user_id} 
        return hb

class User_Hobbies(db.Model):
    """User Hobbie model of dating website"""

    __tablename__ = "user_hobbies"

    user_hobbie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hobbie_id = db.Column(db.Integer,db.ForeignKey('hobbies.hobbie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    

    #relationship
    user = db.relationship('User')
    hobbie = db.relationship('Hobbie')


    def __repr__(self):

        """ Provide helpful representation when printed """
        uhb = f"""<User_hobbie  hobbie_id ={self.hobbie_id}
                                user_id ={self.user_id} >"""
        return uhb

class Like(db.Model):
    """like model of dating website"""

    __tablename__ = "likes"


    like_id= db.Column(db.Integer, autoincrement = True, primary_key = True) 
    likes_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    liked_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    #relationship
    likes_user = db.relationship('User', foreign_keys=[likes_user_id], backref="likes")
    liked_user = db.relationship('User', foreign_keys=[liked_user_id], backref="liked")

    def __repr__(self):

        """ Provide helpful representation when printed """
        lk = f"""<like  like_id ={self.like_id}
                        likes_user ={self.likes_user} 
                        liked_user={self.liked_user}>"""
        return lk

class Dislike(db.Model):
    """dislike model of dating website"""

    __tablename__ = "dislikes"


    dislike_user_id= db.Column(db.Integer, autoincrement = True, primary_key = True) 
    dislikes_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    disliked_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    #relationship
    dislikes_user = db.relationship('User', foreign_keys=[dislikes_user_id], backref="dislikes")
    disliked_user = db.relationship('User', foreign_keys=[disliked_user_id], backref="disliked")

    def __repr__(self):

        """ Provide helpful representation when printed """
        dl = f"""<Dislike   dislike_id ={self.dislike_user_id}
                            dislikes ={self.dislikes_user} 
                            disliked={self.disliked_user}>"""
        return dl

class Image(db.Model):
    """image model"""

    __tablename__="images"

    image_id = db.Column(db.Integer, autoincrement = True, primary_key = True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    url = db.Column(db.String(200), nullable=False)

    #relationship
    user = db.relationship('User')

    def __repr__(self):

        """ Provide helpful representation when printed """
        im = f"""<Image  image_id ={self.image_id}
                        user_id ={self.user_id} 
                        url={self.url}>"""
        return im

##############################################################################
    # Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dating'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":

    #from server import app
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")


"""Utility file to seed dating database """

import datetime
from sqlalchemy import func

from model import User,Hobbie,Like,Dislike,Image,connect_to_db,db 
# from server import app


def load_users():

    """Create example data for the test database."""

    # User.query.delete()

    user1 = User(fname="Deepika ",lname="Padukone",email="dp@gmail.com",
                password="dp111",age=32, gender="F",city="Mumbai",state="MH",
                contact_no="4084536679",occupation="Actress")

    user2 = User(fname="Ranvir ",lname="Singh",email="rv@gmail.com",
                password="rv222",age=30, gender="M",city="Mumbai",state="MH",
                contact_no="4082222679",occupation="Actor")

    user3 = User(fname="Diya ",lname="Mirza",email="dm@hotmail.com",
                password="dm444",age=38, gender="F",city="Delhi",state="DL",
                contact_no="4084544445",occupation="Fashion Designer")

    user4 = User(fname="Katrina ",lname="Kaif",email="kf@yahoo.com",
                password="kf000",age=30, gender="F",city="Chandigarh",state="CH",
                contact_no="9421366790",occupation="Actress")

    user5 = User(fname="Esha ",lname="Gupta",email="eg@gmail.com",
                password="eg999",age=35, gender="F",city="Goa",state="GA",
                contact_no="9427158913",occupation="Engineer")

    user6 = User(fname="Hrithik ",lname="Roshan",email="hr@outlook.com",
                password="hr123",age=40, gender="M",city="Gujarat",state="GJ",
                contact_no="9227155913",occupation="Actor")

    user7 = User(fname="Akshay ",lname="Kumar",email="ak@gmail.com",
                password="ak47",age=42, gender="M",city="Rajesthan",state="RJ",
                contact_no="9997188913",occupation="Actor")

    db.session.add_all([user1, user2, user3,user4,user5,user6,user7])
    db.session.commit()

    hobbie1 = Hobbie(user=user2,hobbie_name="singing")
    hobbie2 = Hobbie(user=user3,hobbie_name="dancing")
    hobbie3 = Hobbie(user=user5,hobbie_name="drawing")
    hobbie4 = Hobbie(user=user6,hobbie_name="cooking")

    db.session.add_all([hobbie1, hobbie2, hobbie3,hobbie4])
    db.session.commit()

    like1 = Like(likes_user = user2,liked_user=user4)
    like2 = Like(likes_user = user5,liked_user= user4)
    like3 = Like(likes_user = user5,liked_user= user2)
    like4 = Like(likes_user = user2,liked_user= user5)
    like5 = Like(likes_user = user3,liked_user= user4)

    db.session.add_all([like1, like2, like3,like4,like5])
    db.session.commit()

    dlike1 = Dislike(dislikes = user2,disliked= user4)
    dlike2 = Dislike(dislikes = user3,disliked= user4)
    dlike3 = Dislike(dislikes = user5,disliked= user4)
    dlike4 = Dislike(dislikes = user5,disliked= user3)

    db.session.add_all([dlike1, dlike2, dlike3,dlike4])
    db.session.commit()

    img1 = Image(user_id=2,url="xyz")
    img2 = Image(user_id=3,url="abc")
    img3 = Image(user_id=1,url="pqy")
    img4 = Image(user_id=4,url="vvv")

    db.session.add_all([img1, img2, img3,img4])
    db.session.commit()


def seed_data():

    load_users()



if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
    seed_data()













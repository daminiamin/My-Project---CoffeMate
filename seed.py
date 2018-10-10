
"""Utility file to seed dating database """

import datetime
from sqlalchemy import func

from model import User,Hobbie,Like,Dislike,Image,connect_to_db,db 
# from server import app


def load_users():

    """Create example data for the test database."""

    # User.query.delete()

    deepika = User(fname="Deepika ",lname="Padukone",email="dp@gmail.com",
                password="dp111",age=32, gender="F",city="Mumbai",state="MH",
                contact_no="4084536679",occupation="Actress")

    ranvir = User(fname="Ranvir ",lname="Singh",email="rv@gmail.com",
                password="rv222",age=30, gender="M",city="Mumbai",state="MH",
                contact_no="4082222679",occupation="Actor")

    diya = User(fname="Diya ",lname="Mirza",email="dm@hotmail.com",
                password="dm444",age=38, gender="F",city="Delhi",state="DL",
                contact_no="4084544445",occupation="Fashion Designer")

    katrina = User(fname="Katrina ",lname="Kaif",email="kf@yahoo.com",
                password="kf000",age=30, gender="F",city="Chandigarh",state="CH",
                contact_no="9421366790",occupation="Actress")

    esha = User(fname="Esha ",lname="Gupta",email="eg@gmail.com",
                password="eg999",age=35, gender="F",city="Goa",state="GA",
                contact_no="9427158913",occupation="Engineer")

    hrithik = User(fname="Hrithik ",lname="Roshan",email="hr@outlook.com",
                password="hr123",age=40, gender="M",city="Gujarat",state="GJ",
                contact_no="9227155913",occupation="Actor")

    akshay = User(fname="Akshay ",lname="Kumar",email="ak@gmail.com",
                password="ak47",age=42, gender="M",city="Rajesthan",state="RJ",
                contact_no="9997188913",occupation="Actor")

    db.session.add_all([deepika,ranvir, diya,katrina,esha,hrithik,akshay])
    db.session.commit()

    hobbie1 = Hobbie(user=deepika,hobbie_name="singing")
    hobbie2 = Hobbie(user=ranvir,hobbie_name="dancing")
    hobbie3 = Hobbie(user=akshay,hobbie_name="drawing")
    hobbie4 = Hobbie(user=esha,hobbie_name="cooking")

    db.session.add_all([hobbie1, hobbie2, hobbie3,hobbie4])
    db.session.commit()

    like1 = Like(likes_user = deepika,liked_user=hrithik)
    like2 = Like(likes_user = ranvir,liked_user= esha)
    like3 = Like(likes_user = akshay,liked_user= katrina)
    like4 = Like(likes_user = katrina,liked_user= ranvir)
    like5 = Like(likes_user = esha,liked_user= katrina)

    db.session.add_all([like1, like2, like3,like4,like5])
    db.session.commit()

    dlike1 = Dislike(dislikes_user = deepika,disliked_user= katrina)
    dlike2 = Dislike(dislikes_user = akshay,disliked_user= katrina)
    dlike3 = Dislike(dislikes_user = esha,disliked_user= hrithik)
    dlike4 = Dislike(dislikes_user = akshay,disliked_user= ranvir)

    db.session.add_all([dlike1, dlike2, dlike3,dlike4])
    db.session.commit()

    img1 = Image(user=akshay,url="xyz")
    img2 = Image(user=katrina,url="abc")
    img3 = Image(user=diya,url="pqy")
    img4 = Image(user=esha,url="vvv")

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













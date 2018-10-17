
"""Utility file to seed dating database """

import datetime
from sqlalchemy import func

from model import User,Hobbie,User_Hobbies,Like,Dislike,Image,connect_to_db,db 
# from server import app


def load_users():

    """Create example data for the test database."""

    Like.query.delete()
    Dislike.query.delete()
    User_Hobbies.query.delete()
    Image.query.delete()
    User.query.delete()
    Hobbie.query.delete()


    deepika = User(fname="Deepika ",lname="Padukone",email="dp@gmail.com",
                password="dp111",age=32, gender="F",interested_in ="M",
                city="Mumbai",state="MH",contact_no="4084536679",
                occupation="Actress")

    diya = User(fname="Diya ",lname="Mirza",email="dm@hotmail.com",
                password="dm444",age=38, gender="F",interested_in ="M",
                city="Delhi",state="DL",contact_no="4084544445",
                occupation="Fashion Designer")

    akshay = User(fname="Akshay ",lname="Kumar",email="ak@gmail.com",
                password="ak47",age=42, gender="M",interested_in ="F",
                city="Rajesthan",state="RJ",contact_no="9997188913",
                occupation="Actor")

    katrina = User(fname="Katrina ",lname="Kaif",email="kf@yahoo.com",
                password="kf000",age=30, gender="F",interested_in ="M",
                city="Chandigarh",state="CH",contact_no="9421366790",
                occupation="Actress")

    ranvir = User(fname="Ranvir ",lname="Singh",email="rv@gmail.com",
                password="rv222",age=30, gender="M",interested_in ="F",
                city="Mumbai",state="MH",contact_no="4082222679",
                occupation="Actor")

    esha = User(fname="Esha ",lname="Gupta",email="eg@gmail.com",
                password="eg999",age=35, gender="F",interested_in ="M",city="Goa"
                ,state="GA",contact_no="9427158913",occupation="Engineer")

    hrithik = User(fname="Hrithik ",lname="Roshan",email="hr@outlook.com",
                password="hr123",age=40, gender="M",interested_in ="F",
                city="Gujarat",state="GJ",contact_no="9227155913",
                occupation="Actor")

   

    db.session.add_all([deepika,ranvir, diya,katrina,esha,hrithik,akshay])
    db.session.commit()


    hobbie1 = Hobbie(hobbie_name="singing")
    hobbie2 = Hobbie(hobbie_name="dancing")
    hobbie3 = Hobbie(hobbie_name="cooking")
    hobbie4 = Hobbie(hobbie_name="drawing")
    hobbie5 = Hobbie(hobbie_name="knitting")

    db.session.add_all([hobbie1, hobbie2, hobbie3,hobbie4,hobbie5])
    db.session.commit()
    

    deepika.hobbies.extend([hobbie4])
    ranvir.hobbies.append(hobbie4)
    akshay.hobbies.append(hobbie4)
    esha.hobbies.append(hobbie3)
    esha.hobbies.append(hobbie4)
    akshay.hobbies.append(hobbie3)
    katrina.hobbies.append(hobbie5)
    deepika.hobbies.append(hobbie5)


    db.session.commit()
    # deepika.likes.append(hrithik)
    like1 = Like(likes_user = deepika,liked_user=hrithik)
    like2 = Like(likes_user = ranvir,liked_user= hrithik)
    like3 = Like(likes_user = akshay,liked_user= katrina)
    like4 = Like(likes_user = katrina,liked_user= ranvir)
    like5 = Like(likes_user = esha,liked_user= katrina)
    like6 = Like(likes_user = esha,liked_user= hrithik)


    db.session.add_all([like1, like2, like3,like4,like5,like6])
    db.session.commit()

    dlike1 = Dislike(dislikes_user = deepika,disliked_user= katrina)
    dlike2 = Dislike(dislikes_user = akshay,disliked_user= katrina)
    dlike3 = Dislike(dislikes_user = esha,disliked_user= hrithik)
    dlike4 = Dislike(dislikes_user = akshay,disliked_user= katrina)
    dlike5 = Dislike(dislikes_user = akshay,disliked_user= katrina)
    dlike6 = Dislike(dislikes_user = akshay,disliked_user= esha)


    db.session.add_all([dlike1, dlike2, dlike3,dlike4,dlike5,dlike6])
    db.session.commit()

    img1 = Image(user=akshay,url="http://www.gstatic.com/tv/thumb/persons/90028/90028_v9_ba.jpg")
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














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


    deepika = User(fname="Deepika",lname="Padukone",email="d@gmail.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=32, gender="F",interested_in ="M",
                city="Santa Clara",state="CA",contact_no="9421853667",
                occupation="Actress")

    shahid = User(fname="Shahid ",lname="Kapoor",email="sh@hotmail.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=38, gender="M",interested_in ="F",
                city="Portland",state="OR",contact_no="4084544445",
                occupation="Fashion Designer")

    akshay = User(fname="Akshay ",lname="Kumar",email="ak@gmail.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=42, gender="M",interested_in ="F",
                city="Los Angeles",state="CA",contact_no="9997188913",
                occupation="Actor")

    ranvir = User(fname="Ranvir ",lname="Singh",email="rv@gmail.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=30, gender="M",interested_in ="F",
                city="San Francisco",state="CA",contact_no="4082222679",
                occupation="Actor")

    rani = User(fname="Rani ",lname="Mukherjee",email="rn@gmail.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=35, gender="F",interested_in ="M",city="Atlanta"
                ,state="GA",contact_no="9427158913",occupation="Engineer")

    hrithik = User(fname="Hrithik ",lname="Roshan",email="hr@outlook.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=40, gender="M",interested_in ="F",
                city="Palo Alto",state="CA",contact_no="9227155913",
                occupation="Actor")
    ranbir = User(fname="Ranbir ",lname="Kapoor",email="rk@gmail.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=18, gender="M",interested_in ="F",
                city="Palo Alto",state="CA",contact_no="9223559199",
                occupation="Actor")
    shahrukh = User(fname="Shahrukh ",lname="Khan",email="sk@gmail.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=18, gender="M",interested_in ="F",
                city="Palo Alto",state="CA",contact_no="9223559145",
                occupation="Actor")
    aish = User(fname="Aishwarya ",lname="Rai",email="as@gmail.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=35, gender="F",interested_in ="M",city="Atlanta"
                ,state="GA",contact_no="9427158911",occupation="Actress")

    sonam = User(fname="Sonam ",lname="Kapoor",email="snk@gmail.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                age=35, gender="F",interested_in ="M",city="Atlanta"
                ,state="GA",contact_no="9427158914",occupation="Designer")

    katrina = User(fname="Katrina ",lname="Kaif",email="kf@yahoo.com",
                password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
                ,age=30, gender="F",interested_in ="M",
                city="Destin",state="FL",contact_no="9421366790",
                occupation="Actress")


   

    db.session.add_all([deepika,shahid,akshay,ranvir,rani,hrithik,ranbir,shahrukh,aish,sonam,katrina])
    db.session.commit()


    hobbie1 = Hobbie(hobbie_name="Travel")
    hobbie2 = Hobbie(hobbie_name="Yoga")
    hobbie3 = Hobbie(hobbie_name="Reading")
    hobbie4 = Hobbie(hobbie_name="Fishing")
    hobbie5 = Hobbie(hobbie_name="Cricket")
    hobbie6 = Hobbie(hobbie_name="Swimming")
    hobbie7 = Hobbie(hobbie_name="Gardening")



    db.session.add_all([hobbie1, hobbie2, hobbie3,hobbie4,hobbie5,hobbie6,hobbie7])
    db.session.commit()
    

    deepika.hobbies.extend([hobbie4,hobbie2,hobbie3,hobbie7]) #extends stores
    shahid.hobbies.append(hobbie3)
    akshay.hobbies.append(hobbie4)
    ranvir.hobbies.extend([hobbie4,hobbie6])
    rani.hobbies.append(hobbie3)
    hrithik.hobbies.extend([hobbie7,hobbie1,hobbie4])
    ranbir.hobbies.extend([hobbie1,hobbie4,hobbie7])
    shahrukh.hobbies.extend([hobbie1,hobbie2,hobbie3,hobbie5,hobbie6,hobbie7])
    aish.hobbies.extend([hobbie1,hobbie7])
    sonam.hobbies.append(hobbie5)
    katrina.hobbies.append(hobbie5)



    db.session.commit()
    # deepika.likes.append(hrithik)
    like1 = Like(likes_user = deepika,liked_user=hrithik)
    like2 = Like(likes_user = hrithik,liked_user= deepika)
    like3 = Like(likes_user = akshay,liked_user= rani)
    like4 = Like(likes_user = ranvir,liked_user= deepika)
    like5 = Like(likes_user = ranbir,liked_user= aish)
    like6 = Like(likes_user = sonam,liked_user= hrithik)


    db.session.add_all([like1, like2, like3,like4,like5,like6])
    db.session.commit()

    dlike1 = Dislike(dislikes_user = deepika,disliked_user= katrina)
    dlike2 = Dislike(dislikes_user = akshay,disliked_user= katrina)
    dlike3 = Dislike(dislikes_user = rani,disliked_user= katrina)
    dlike4 = Dislike(dislikes_user = akshay,disliked_user= sonam)
    dlike5 = Dislike(dislikes_user = ranvir,disliked_user= rani)
    dlike6 = Dislike(dislikes_user = shahid,disliked_user= rani)


    db.session.add_all([dlike1, dlike2, dlike3,dlike4,dlike5,dlike6])
    db.session.commit()

    img1 = Image(user=deepika,filename="1_dp.png")
    img2 = Image(user=shahid,filename="2_sh.png")
    img3 = Image(user=akshay,filename="3_ak.png")
    img4 = Image(user=ranvir,filename="4_rv.png")
    img5 = Image(user=rani,filename="5_rn.png")

    img6 = Image(user=hrithik,filename="6_hr.png")
    img7 = Image(user=ranbir,filename="7_rk.png")

    img8 = Image(user=shahrukh,filename="7_sk.png")
    img9 = Image(user=aish,filename="8_as.png")
    img10 = Image(user=sonam,filename="9_snk.png")



    db.session.add_all([img1,img2,img3,img4,img5,img6,img7,img8,img9,img10])
    db.session.commit()
    #making profile pic saparate 
    deepika.profile = img1
    shahid.profile = img2
    akshay.profile = img3
    ranvir.profile = img4

    rani.profile = img5
    hrithik.profile = img6
    ranbir.profile = img7
    shahrukh.profile = img8
    aish.profile = img9
    sonam.profile = img10

    db.session.commit()


def seed_data():

    load_users()



if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
    seed_data()













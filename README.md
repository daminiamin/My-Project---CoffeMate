
# Coffee Mate :coffee::hearts:

This is a Dating website which allows users to find their matches and filter their connections by liking or disliking profiles. Users can connect by sending emails (using the OAuth and Gmail APIs) & Phone Number. The site also suggests near by coffee shops (using the Yelp API and GeoPy Library) where matched users can go for a coffee date.


## Table of Contents

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)



## <a name="tech-stack"></a>Tech Stack

__Frontend:__ HTML5, CSS, Jinja,Javascript, AJAX, JSON, jQuery, Bootstrap <br/>
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy ORM, <br/>
__APIs:__ Google Oauth, Gmail , Yelp <br/>

## <a name="features">Features

*  Signup       
*  Login 
*  Homepage
*  See users Suggestions based on their hobbies/gender preference
*  Like/Unlike, Dislike/Undislike to each other
*  Suggestion Of Coffee Shops based on midpoint beatween their location
*  Access of Sending Email/ Phone number if it's a Match



## <a name="installation"></a>Setup/Installation ⌨️

#### Requirements:

- PostgreSQL
- Python 3
- Yelp and Google OAuth API keys


To have Coffee Mate running on your local computer, please follow the below steps:


Clone repository:
```
$ git clone https://github.com/daminiamin/CoffeeMate.git
```
Create a virtual environment🔮:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies🔗:
```
$ pip3 install -r requirements.txt
```

Get your own secret keys🔑 for [Yelp](https://www.yelp.com/developers) and [Google OAuth](https://developers.google.com/gmail/api/auth/web-server). Save them to a file `secrets.sh`. 

Create database 'dating'.
```
$ createdb dating
```
Create your database tables and seed example data.
```
$ python3 model.py
```
Run the app from the command line.
```
$ python3 server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python3 -i model.py
```

## Authors

* :gift_heart: ** Damini Amin ** :gift_heart:- *Initial work* -

## Acknowledgments

* credits :credit_card:

    - https://unsplash.com/
    - https://www.pexels.com/
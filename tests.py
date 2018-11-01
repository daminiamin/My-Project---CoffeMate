import unittest
from io import BytesIO  # upload file

from server import app
import server

from model import db, connect_to_db, User
from seed import load_users 


class MyAppIntegrationTestCase(unittest.TestCase):
    """Testing of integration tests: testing Flask server."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_landingpage(self):
        """ Checking landing page"""
        result = self.client.get('/')
        self.assertIn(b'Coffe Mate', result.data) #checking data on page
        self.assertIn(b'Login', result.data) #checking data on page

        self.assertIn(b'SignUp', result.data) #checking data on page

        self.assertEqual(result.status_code, 200)#checking code

    # def test_allowed_file(self,filename):
    #     """ Checking files allowed to upload"""
    #     result = self.client.get()

###################### LoggedinTests ############################

class LoggedInTestCase(unittest.TestCase):
    """Testing of logged out /assume user already logged in """


    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET KEY'] = 'key'

        connect_to_db(app, "postgresql:///testdb")

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        db.create_all()
        load_users()


    def test_login(self):
        """ Checking login successfully"""

        result = self.client.post('/login',
                                  data={'email': 'd@gmail.com',
                                        'password':'123'}, 
                                  follow_redirects=True) #make it false to check data

        self.assertIn(b'Logged in', result.data)
        # self.assertEqual(sess['user_id'], 1)

    def test_logout(self):
        """ Checking logout """
        result = self.client.get('/logout', follow_redirects=True)

        self.assertIn(b"Coffe Mate",result.data)

        self.assertNotIn(b"Nice to meet you ",result.data)

    def test_visit_profile(self):
        """ Checking another user's profile"""

        result = self.client.get('/profile/1', follow_redirects=True)

        self.assertIn(b"City",result.data)

        self.assertNotIn(b"Visit profile",result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
    
###################### LoggedOutTests ############################

class LoggedOutTestCase(unittest.TestCase):
    """Testing of logged in/ user is not logged in yet """


    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")
      
        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        load_users()



    def test_wrong_email(self):
        """Checking wrong email"""
        result = self.client.post('/login',
                                  data={'email': 'dpdg@gmail.com',
                                        'password':'123'}, 
                                  follow_redirects=True)
        self.assertIn(b'No such user', result.data)

    def test_wrong_pswd(self):
        """Checking wrong password"""

        result = self.client.post('/login',
                                  data={'email': 'd@gmail.com',
                                        'password':'d111'}, 
                                  follow_redirects=True)
        self.assertIn(b'Incorrect password', result.data)



    def test_email_exist(self):
        """ checking email exists in database """
        result = self.client.post('/set-up',
                                        data={'fname': 'Deepika',
                                        'lname':'Padukon',
                                        'email': 'd@gmail.com',
                                        'password':'123'}, 
                                  follow_redirects=True)

        self.assertIn(b'User already exists', result.data)




    def test_signup(self):
        """Checking set-up page redirecting to add-user page"""

        result = self.client.post('/set-up',
                                  data={'fname': 'Damini',
                                        'lname':'Amin',
                                        'email': 'amindamini@gmail.com',
                                        'password':'123'}, 
                                  follow_redirects=True)
        self.assertIn(b'create you profile', result.data)

    def test_add_user(self):
        """Checking add user redirecting to homepage"""
        

        with self.client as c:
            with c.session_transaction() as sess:

                sess["fname"]='Damini'
                sess["lname"]='Amin'
                sess["email"]='amindamini@gmail.com'
                sess["password"]='123'

        # import pdb; pdb.set_trace()

        result = self.client.post('/add-user',
                                  content_type='multipart/form-data',#add image
                                  data={'age': 21,
                                        'gender':'F',
                                        'interested_in': 'M',
                                        'city':'Santa Clara',
                                        'state': 'CA',
                                        'contact':'4086432344',
                                        'occupation': 'Engineer',
                                        'hobbie':[1,2],
                                        'aboutme': 'I am nature lover',
                                        'file':(BytesIO(b"abcdef"), 'test.jpg')} #uploading image
                                        ,follow_redirects=True)
        self.assertIn(b'Nice to meet you ', result.data)

        # checking user exists in database 
        DB_result = User.query.filter_by(fname = "Damini").first()
        self.assertIsNotNone(DB_result) #testing that the returned result is not NONE
        self.assertEqual(DB_result.fname, 'Damini') #testing restaurant name is what it should be


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


####################### MOCK TESTS #######################

class Mock_FlaskTests(unittest.TestCase):
   #Tests that require API and user to be in session (logged in)

    def setUp(self):
       """Stuff to do before every test."""

       # Get the Flask test client
       self.client = app.test_client()

       # Show Flask errors that happen during tests
       app.config['TESTING'] = True

       # Connect to test database
       connect_to_db(app, "postgresql:///testdb")

       # Create tables and add sample data
       db.create_all()
       load_users()

       with self.client as c:
           with c.session_transaction() as sess:
               sess['user_id'] = 1


    # Make mock
    def _mock_get_businesses_by_city(coordinates):
        return {'businesses': [{'id': '07EoYzpl0cTz0oCnId0hOA', 'alias': 'dana-street-roasting-company-mountain-view',
            'name': 'Dana Street Roasting Company', 'image_url': 'https://s3-media1.fl.yelpcdn.com/bphoto/bfML1q6JkAKLJpjInLx18g/o.jpg', 
            'is_closed': False, 'url': 'https://www.yelp.com/biz/dana-street-roasting-company-mountain-view?adjust_creative=t03VyWzUVfYmAQ1I-T5_sA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=t03VyWzUVfYmAQ1I-T5_sA', 
            'review_count': 519, 'categories': [{'alias': 'coffee', 'title': 'Coffee & Tea'}, {'alias': 'cafes', 'title': 'Cafes'}, {'alias': 'coffeeroasteries', 'title': 'Coffee Roasteries'}], 'rating': 4.0, 
            'coordinates': {'latitude': 37.39246, 'longitude': -122.07892}, 'transactions': [], 'price': '$', 'location': {'address1': '744 W Dana St', 'address2': '', 'address3': '', 'city': 'Mountain View', 'zip_code': '94041', 'country': 'US', 
            'state': 'CA', 'display_address': ['744 W Dana St', 'Mountain View, CA 94041']}, 
            'phone': '+16503909638', 'display_phone': '(650) 390-9638', 'distance': 1988.328730669314}]}
    
    server.yelp_api = _mock_get_businesses_by_city

    def test_api_data(self):
        """ Checking another user's profile"""

        result = self.client.get('/profile/6')

        self.assertIn(b"Dana",result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all() 

if __name__ == "__main__":
    unittest.main()




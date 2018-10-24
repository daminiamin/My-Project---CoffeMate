import unittest
from io import BytesIO  # upload file

from server import app

from model import db, connect_to_db
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


class LoggedInTestCase(unittest.TestCase):
    """Testing of logged out /assume user already logged in """


    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")
       # test session 
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        load_users()

    def test_logout(self):
        """ Checking logout """
        result = self.client.get('/logout', follow_redirects=True)

        self.assertIn(b"Coffe Mate",result.data)

        self.assertNotIn(b"Nice to meet you ",result.data)

    # def test_visit_profile(self):
    #     """ Checking another user's profile"""
    #     result = self.client.get('/homepage', follow_redirects=True)
    
# ################################################

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


    def test_login(self):
        """ Checking login successfully"""
        result = self.client.post('/login',
                                  data={'email': 'dp@gmail.com',
                                        'password':'dp111'}, 
                                  follow_redirects=True)
        # check that user id is in session
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['user_id'], 1)
            self.assertIn(b'Nice to meet you !', result.data)


    def test_wrong_email(self):
        """Checking wrong email"""
        result = self.client.post('/login',
                                  data={'email': 'd@gmail.com',
                                        'password':'dp111'}, 
                                  follow_redirects=True)
        self.assertIn(b'No such user', result.data)

    def test_wrong_pswd(self):
        """Checking wrong password"""

        result = self.client.post('/login',
                                  data={'email': 'dp@gmail.com',
                                        'password':'d111'}, 
                                  follow_redirects=True)
        self.assertIn(b'Incorrect password', result.data)



    def test_email_exist(self):
        """ checking email exists in database """
        result = self.client.post('/set-up',
                                        data={'fname': 'Deepika',
                                        'lname':'Padukon',
                                        'email': 'dp@gmail.com',
                                        'password':'dp111'}, 
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

    # def test_add_user(self):
    #     """Checking add user redirecting to homepage"""
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess["fname"]='Damini'
    #             sess["lname"]='Amin'
    #             sess["email"]='amindamini@gmail.com'
    #             sess["password"]='123'


    #     result = self.client.post('/add-user',
    #                               content_type='multipart/form-data',#add image
    #                               data={'age': 21,
    #                                     'gender':'F',
    #                                     'interested_in': 'M',
    #                                     'city':'Santa Clara',
    #                                     'state': 'CA',
    #                                     'contact':'4086432344',
    #                                     'occupation': 'Engineer',
    #                                     'hobbie':[1,2],
    #                                     'aboutme': 'I am nature lover',
    #                                     'file':(BytesIO(b"abcdef"), 'test.jpg') #uploading image
    #                                     },follow_redirects=True)
        
    #     self.assertIn(b'Nice to meet you ', result.data)




        """ Check file selected or not """
        # flash('No selected file')
        


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

        # TODO : need to write queries to check database data
        # make redirects false

if __name__ == "__main__":
    unittest.main()






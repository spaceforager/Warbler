"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()
        
        self.user_1 = User.signup(username="testuser",
                            email="test@test.com",
                            password="testuser",
                            image_url=None)
        self.user_1.id = 9700
        uid1 = self.user_1.id 
        
        self.user_2 = User.signup(username="testuser1",
                            email="test1@test.com",
                            password="testuser123",
                            image_url=None)
        
        self.user_2.id = 8765
        uid2 = self.user_2.id
        
        db.session.commit()
        
        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.client = app.test_client()
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test1234@test.com",
            username="testuser1234",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        
    ############## Following/Follows Tests ##############
    
    def test_follows_user(self):
        self.user_1.following.append(self.user_2)
        db.session.commit()
        
        self.assertEqual(len(self.user_1.following), 1)
        self.assertEqual(len(self.user_2.followers), 1)
        self.assertEqual(len(self.user_1.followers), 0)
        self.assertEqual(len(self.user_2.following), 0)
        
        self.assertEqual(self.user_2.followers[0].id, self.user_1.id)
        
    def test_is_following(self):
        self.user_1.following.append(self.user_2)
        db.session.commit()
        
        self.assertTrue(self.user_1.is_following(self.user_2))
        self.assertFalse(self.user_2.is_following(self.user_1))
        
    def test_is_followed_by(self):
        self.user_1.following.append(self.user_2)
        db.session.commit()

        self.assertTrue(self.user_2.is_followed_by(self.user_1))
        self.assertFalse(self.user_1.is_followed_by(self.user_2))
        
    ############## Signup Tests ##############
    
    def test_correct_signup(self):
        test_user = User.signup('test1', 'test1@gmail.com', 'topsecretpassword', None)
        tuid = 43958
        test_user.id = tuid 
        db.session.commit()
        
        user = User.query.get(tuid)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'test1')
        self.assertEqual(user.email, 'test1@gmail.com')
        self.assertNotEqual(user.password, 'topsecretpassword')
        self.assertTrue(user.password.startswith('$2b$'))
    

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "test@test.com", "password", None)
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", None, "password", None)
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "", None)
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", None, None)
    
    
    ############## Authentication Tests ##############
    
    def test_valid_authentication(self):
        user = User.authenticate(self.user_1.username, "testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user_1.id)
        
    def test_invalid_username_auth(self):
        self.assertFalse(User.authenticate("badusername", "password"))
        
    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.user_1.username, "badpassword"))
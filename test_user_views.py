"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows
from bs4 import BeautifulSoup

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Tests for user views"""
    
    def setUp(self):
        
        """Add sample data and create test client"""
        
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()
        
        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        
        self.testuser_id = 23948
        self.testuser.id = self.testuser_id
        
        self.user_1 = User.signup(username="testuser1",
                                    email="test1@test.com",
                                    password="testuser123",
                                    image_url=None)
        self.user_1_id = 3495
        self.user_1.id = self.user_1_id
        
        self.user_2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="testuser8439",
                                    image_url=None)
        
        self.user_2_id = 9899
        self.user2.id = self.user_2_id 
        
        self.user_3 = User.signup(username="testuser3",
                                    email="test3@test.com",
                                    password="testuser20390",
                                    image_url=None)
        
        self.user_4 = User.signup(username="testuser4",
                                    email="test4@test.com",
                                    password="testuser45834",
                                    image_url=None)
        
        db.session.commit()
        
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res 
    
            
    def test_users_index(self):
        
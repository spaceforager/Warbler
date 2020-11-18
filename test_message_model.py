"""Message model tests"""

import os 
from unittest import TestCase
from sqlalchemy import exc 

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app 

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserModelTestCase(TestCase):
    """Tests for message model"""
    
    def setUp(self):
        """Create test client and add sample test data"""
        db.drop_all()
        db.create_all()
        
        self.user_id = 54763
        user = User.signup("testing", "test@testing.com", "password", None)
        user.id = self.user_id
        db.session.commit()
        
        self.user = User.query.get(self.user_id)
        
        self.client = app.test_client()
        
    def tearDown(self):
        result = super().tearDown()
        db.session.rollback()
        return result 
    
    def test_message_model(self):
        """Check if basic model works"""
        
        message = Message(
            text="testing",
            user_id=self.user_id
        )
        
        db.session.add(message)
        db.session.commit()
        
        # user should have 1 message 
        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.user.messages[0].text, "testing")
        
    def test_message_likes(self):
        
        msg_1 = Message(
            text="testing1",
            user_id=self.user_id
        )
    
        msg_2 = Message(
            text="testing2",
            user_id = self.user_id
        )
        
        new_user = User.signup("test1", "testing@email.com", "password", None)
        new_id = 9328
        new_user.id = new_id
        db.session.add_all([msg_1, msg_2, new_user])
        db.session.commit()
        
        new_user.likes.append(msg_1)
        db.session.commit()
        
        like = Likes.query.filter(Likes.user_id == new_user.id).all()
        self.assertEqual(len(like), 1)
        self.assertEqual(like.message_id, msg_1.id)
        
        
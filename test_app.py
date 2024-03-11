from app import app
from unittest import TestCase
import unittest
from models import db, User#, connect_db



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
#connect_db(app)
db.drop_all()
db.create_all()

class userTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        user = User(first_name='userFirstName',last_name='userLastName',image_url='https://images.unsplash.com/photo-1682686581797-21ec383ead02?q=80&w=1587&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<h1 class="text-center">Bogly home page</h1>',html)

    def test_users_list(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>Users</h1>',html)

    def test_new_user(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>Create a User</h1>',html)

    def test_show_user(self):
        with app.test_client() as client:
            user = User(first_name='lolo',last_name='melon',image_url='https://images.unsplash.com/photo-1682686581797-21ec383ead02?q=80&w=1587&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id
            res = client.get(f"users/{self.user_id}") 
            html = res.get_data(as_text=True)   
            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>lolo melon</h1>',html) 

    def test_add_user(self):
        with app.test_client() as client:
            user = {'first_name':'chocolate','last_name':'candy','image_url':'https://images.unsplash.com/photo-1682686581797-21ec383ead02?q=80&w=1587&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'}
            res = client.post('/users/new',data=user,follow_redirects=True)
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>Users</h1>',html)
            
               

if __name__ == '__main__':
    unittest.main()
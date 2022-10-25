import os
import unittest

from views import app, db, login, register
from _config import basedir
from models import User

TEST_DB = 'test.db'

class Alltests(unittest.TestCase):
    #execute prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,TEST_DB)
        self.app = app.test_client()
        db.create_all()

	#executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    #helper methods
    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)
    
    def register(self,name, email, password, confirm):
        return self.app.post('/register',
               data=dict(name=name, email=email,password=password,confirm=confirm),
               follow_redirects=True)
    
    def logout(self):
        return self.app.get('/logout',follow_redirects=True)

    def create_user(self,name,email,password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
    
    def create_task(self):
        return self.app.post('/add', data=dict(
            name="finish classes",
            due_date="02/11/2022",
            priority='1',
            posted_date="25/10/2022",
            status="1"
        ),follow_redirects=True)
    
    #tests
    def test_user_setup(self):
        new_user = User("michael", "michael@mherman.org", "michaelherman")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "michael"
        
    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Please login to access your task list.', response.data)
        
    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo','bar')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_users_can_login(self):
        self.register('ayuri','ayuri@python.org','python','python')
        response = self.login('ayuri','python')
        self.assertIn(b'Welcome',response.data)

    def test_invalid_form_data(self):
        self.register('ayuri','ayuri@python.org','python','python')
        response = self.login('alert("alert box");','foo')
        self.assertIn(b'Invalid username or password',response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('/register',follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please register to access the task list", response.data)
        
    def test_user_registration(self):
        self.app.get('/register',follow_redirects=True)
        self.register('Michael', 'michael@realpython.com','python','python')
        self.app.get('/register',follow_redirects=True)
        response = self.register('Michael', 'michael@realpython.com','python','python')
        self.assertIn(b'That username and/or email already exists.',response.data)
        
    def test_logged_in_users_can_logout(self):
        self.register('Michael', 'michael@realpython.com','python','python')
        self.login('Michael','python')
        response = self.logout()
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Goodbye!',response.data)
    
    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!',response.data)

    def test_logged_in_users_can_access_tasks_page(self):
        self.register('fulano','fulano@python.org','python101','python101')
        self.login('fulano','python101')
        # response = self.app.get('/tasks')
        response = self.app.get('/tasks',follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Add a new task:', response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('/tasks',follow_redirects=True)
        self.assertIn(b'Please login to access your task list.', response.data)
        
    def test_users_can_add_tasks(self):
        self.create_user('Ayuri','ayuri@realpython.org','python')
        self.login('ayuri','python')
        self.app.get('/tasks',follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'New entry was successfully posted. Thanks.', response.data)
        
    def test_users_cannot_add_tasks_when_error(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='',
            priority='1',
            posted_date='02/05/2014',
            status='1'
        ), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)
        

        
        
if __name__ == "__main__":
    unittest.main()
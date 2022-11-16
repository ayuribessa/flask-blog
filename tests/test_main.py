import os
import unittest

from project import app, db
from project ._config import basedir
from project.models import User


TEST_DB = 'test.db'

class MainTests(unittest.TestCase):
     # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.assertEquals(app.debug, False)
        
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()   

  
    ########################
    #### helper methods ####
    ########################

    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)


    ###############
    #### tests ####
    ###############
    
    def test_404_error(self):
        response = self.app.get('/some-fake-route/')
        self.assertEquals(response.status_code, 404)

    def test_500_error(self):
        #add o user no banco sem passar pelo controller de add, portanto sem criptografar
        bad_user = User(
            name='Testing',
            email="user@python.com",
            password="django"
        )
        db.session.add(bad_user)
        db.session.commit()
        response = self.login('Testing', 'django')
        self.assertEquals(response.status, 500)

if __name__ == "__main__":
    unittest.main()
        
  
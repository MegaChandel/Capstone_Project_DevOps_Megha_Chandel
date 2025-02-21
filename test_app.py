import unittest
import json
from app import app, db, User

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

    def test_home(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.app.post('/users',
                                 data=json.dumps({"name": "John Doe", "email": "john@example.com"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_user(self):
        self.app.post('/users',
                      data=json.dumps({"name": "John Doe", "email": "john@example.com"}),
                      content_type='application/json')

        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        self.app.post('/users',
                      data=json.dumps({"name": "John Doe", "email": "john@example.com"}),
                      content_type='application/json')

        response = self.app.put('/users/1',
                                 data=json.dumps({"name": "John Updated", "email": "johnupdated@example.com"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        self.app.post('/users',
                      data=json.dumps({"name": "John Doe", "email": "john@example.com"}),
                      content_type='application/json')

        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == "__main__":
    unittest.main()
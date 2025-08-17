import unittest
from unittest.mock import patch
from app import app, db, Project, Contact
import json

class TestPortfolioApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hero', response.data)
        self.assertIn(b'About', response.data)
        self.assertIn(b'Skills', response.data)
        self.assertIn(b'Contact', response.data)

    def test_projects_gallery(self):
        project = Project(title='Test Project', description='Test Description', technology='React')
        db.session.add(project)
        db.session.commit()

        response = self.app.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Project', response.data)
        self.assertIn(b'Test Description', response.data)
        self.assertIn(b'React', response.data)

    def test_project_details(self):
        project = Project(title='Test Project', description='Test Description', technology='React')
        db.session.add(project)
        db.session.commit()

        response = self.app.get(f'/projects/{project.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Project', response.data)
        self.assertIn(b'Test Description', response.data)
        self.assertIn(b'React', response.data)

    def test_project_filter(self):
        project1 = Project(title='Project 1', description='React Project', technology='React')
        project2 = Project(title='Project 2', description='Flask Project', technology='Flask')
        db.session.add(project1)
        db.session.add(project2)
        db.session.commit()

        response = self.app.get('/projects?technology=React')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project 1', response.data)
        self.assertNotIn(b'Project 2', response.data)

    def test_contact_form(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        }
        response = self.app.post('/contact', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        contact = Contact.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(contact)
        self.assertEqual(contact.name, 'Test User')
        self.assertEqual(contact.message, 'This is a test message.')

    @patch('app.send_email')
    def test_contact_form_email(self, mock_send_email):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        }
        response = self.app.post('/contact', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        mock_send_email.assert_called_once_with('test@example.com', 'New Message from Portfolio Website', data['message'])

    def test_admin_panel(self):
        # Log in as admin
        with self.app.session_transaction() as session:
            session['admin'] = True

        # Create some contact messages
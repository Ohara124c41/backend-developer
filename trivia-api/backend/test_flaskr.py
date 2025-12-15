import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = (
            os.getenv("TEST_DATABASE_URL")
            or os.getenv("DATABASE_URL")
            or "postgresql://postgres@localhost:5432/{}".format(self.database_name)
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()
            self.seed_data()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def seed_data(self):
        category1 = Category(type='Science')
        category2 = Category(type='Art')
        self.db.session.add_all([category1, category2])
        self.db.session.commit()

        question1 = Question(question='What is H2O?', answer='Water', category=category1.id, difficulty=1)
        question2 = Question(question='Who painted Mona Lisa?', answer='Da Vinci', category=category2.id, difficulty=2)
        self.db.session.add_all([question1, question2])
        self.db.session.commit()

    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']))

    def test_get_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_get_questions_404(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_question_success(self):
        new_question = Question(question='Temp?', answer='Temp', category=1, difficulty=1)
        new_question.insert()
        res = self.client().delete(f'/questions/{new_question.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], new_question.id)

    def test_delete_question_404(self):
        res = self.client().delete('/questions/9999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_question_success(self):
        payload = {
            'question': 'New question?',
            'answer': 'New answer',
            'category': 1,
            'difficulty': 2
        }
        res = self.client().post('/questions', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_create_question_400(self):
        res = self.client().post('/questions', json={'question': 'Missing fields'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_search_questions_success(self):
        res = self.client().post('/questions', json={'searchTerm': 'What'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))

    def test_search_questions_empty(self):
        res = self.client().post('/questions', json={'searchTerm': 'xyznotfound'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)

    def test_get_questions_by_category_success(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['current_category'], 'Science')

    def test_get_questions_by_category_404(self):
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_play_quiz_success(self):
        payload = {
            'previous_questions': [],
            'quiz_category': {'id': 0, 'type': 'click'}
        }
        res = self.client().post('/quizzes', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_play_quiz_400(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

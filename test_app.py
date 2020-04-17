import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, Casting
import datetime

JWT_PRODUCER = os.environ['JWT_PRODUCER']
JWT_DIRECTOR = os.environ['JWT_DIRECTOR']
JWT_ASSISTANT = os.environ['JWT_ASSISTANT']


class CastingAgencyAPITestCase(unittest.TestCase):
    """This class represents the casting agency API test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': "I'm a new actor",
            'age': 48,
            'gender': "female"
        }

        self.update_actor = {
            'name': "Alicia Pacino",
            'gender': "female"
        }

        self.new_movie = {
            'title': "2020",
            'release_date': datetime.datetime(2020, 2, 29).strftime('%Y-%m-%d')
        }

        self.update_movie = {
            'title': "Contagion",
            'release_date': datetime.datetime(2020, 5, 7).strftime('%Y-%m-%d')
        }

        self.headers_assistant = {
            'Content-Type': 'application/json', 'Authorization': JWT_ASSISTANT}

        self.headers_director = {
            'Content-Type': 'application/json', 'Authorization': JWT_DIRECTOR}

        self.headers_producer = {
            'Content-Type': 'application/json', 'Authorization': JWT_PRODUCER}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Tests for Actor endpoints and RBAC pass tests

    def test_get_actors(self):
        """Pass GET/actors"""
        res = self.client().get('/actors', headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_requesting_actors(self):
        """Fail GET/actors with malformed endpoint url"""
        res = self.client().get('/actors', headers={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_actor_movies(self):
        """Pass GET/actors/<id>/movies"""
        res = self.client().get('/actors/2/movies', headers=self.headers_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_requesting_actor_movies(self):
        """Fail GET/actors/<id>/movies with malformed endpoint url"""
        res = self.client().get('/actors/2/movies/',  headers=self.headers_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_add_new_actor(self):
        """Pass POST/actors to create a new actor"""
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_400_if_no_body_parameters_provided_to_add_new_actor(self):
        """Fail POST/actors by sending empty json data"""
        res = self.client().post('/actors', json={}, headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_patch_actor(self):
        """Pass PATCH/actors/<id> to update an actor"""
        res = self.client().patch('/actors/1', json=self.update_actor,
                                  headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_if_non_existing_id_provided_to_update_actor(self):
        """Fail PATCH/actors/<id> with non existent id"""
        res = self.client().patch('/actors/9999', json=self.update_actor,
                                  headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_actor(self):
        """Pass DELETE/actors/<id> to delete an actor"""
        res = self.client().delete('/actors/4', headers=self.headers_producer)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'])
        self.assertEqual(actor, None)

    def test_404_if_actor_to_delete_not_found(self):
        """Fail DELETE/actors/<id> with non existent id"""
        res = self.client().delete('/actors/9999', headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for Movie endpoints and RBAC pass tests

    def test_get_movies(self):
        """Pass GET/movies"""
        res = self.client().get('/movies', headers=self.headers_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_requesting_movies(self):
        """Fail GET/movies with malformed endpoint url"""
        res = self.client().get('/movies/', headers=self.headers_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_movie_actors(self):
        """Pass GET/movies/<id>/actors"""
        res = self.client().get('/movies/1/actors', headers=self.headers_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_requesting_actor_movies(self):
        """Fail GET/movies/<id>/actors with malformed endpoint url"""
        res = self.client().get('/movies/1/actors/',  headers=self.headers_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_add_new_movie(self):
        """Pass POST/movies to create a new movie"""
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_400_if_bad_body_parameters_provided_to_add_new_movie(self):
        """Fail POST/movies by sending empty json data"""
        res = self.client().post('/movies', json=self.new_actor,
                                 headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_patch_movie(self):
        """Pass PATCH/movies/<id> to update a movie"""
        res = self.client().patch('/movies/1', json=self.update_movie,
                                  headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_if_non_existing_id_provided_to_update_movie(self):
        """Fail PATCH/movies/<id> with non existent id"""
        res = self.client().patch('/movies/9999', json=self.update_movie,
                                  headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie(self):
        """Pass DELETE/movies/<id> to delete a movie"""
        res = self.client().delete('/movies/2', headers=self.headers_producer)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'])
        self.assertEqual(movie, None)

    def test_404_if_movie_to_delete_not_found(self):
        """Fail DELETE/actors/<id> with non existent id"""
        res = self.client().delete('/movies/9999', headers=self.headers_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for Casting endpoints and RBAC pass tests

    # RBAC fail tests
    def test_404_requesting_actors(self):
        """Fail GET/actors with missing Auth header"""
        res = self.client().get('/actors', headers={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_401_missing_token_requesting_actors(self):
        """Fail GET/actors with missing malformed Auth header"""
        res = self.client().get('/actors',
                                headers={'Content-Type': 'application/json', 'Authorization': "Bearer "})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token not found.')

    def test_403_adding_new_actor_by_assistant(self):
        """Fail POST/movies by assistant role"""
        res = self.client().post('/actors', json=self.new_movie,
                                 headers=self.headers_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_403_adding_new_movie_by_director(self):
        """Fail POST/movies by director role"""
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.headers_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

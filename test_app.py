import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('TEST_DATABASE_URI')
        #"postgres://test:test123@localhost:5432/test_casting_agency"
        setup_db(self.app, self.database_path)
        self.producer_token = os.getenv('PRODUCER_TOKEN')
        self.director_token = os.getenv('DIRECTOR_TOKEN')
        self.assistant_token = os.getenv('ASSISTANT_TOKEN')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_actors_200(self):
        res = self.client().get('/actors',  headers={"Authorization": "Bearer {}".format(self.assistant_token)})
        data = json.loads(res.data)
        actors = [actor.to_dict() for actor in Actor.query.all()]
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actors'], actors) 
        self.assertTrue(data['success'])
    
    def test_get_all_actors_without_token_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Authorization header is expected.")
        
        
    def test_get_actors_405(self):
        res = self.client().delete('/actors')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Method Not Allowed")


    def test_get_all_movies_200(self):
        res = self.client().get('/movies',  headers={"Authorization": "Bearer {}".format(self.assistant_token)})
        data = json.loads(res.data)
        movies = [movie.to_dict() for movie in Movie.query.all()]
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['movies']), len(movies)) 
        self.assertTrue(data['success'])
    
    def test_get_all_movies_without_token_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Authorization header is expected.")
        
        
    def test_get_movies_405(self):
        res = self.client().delete('/movies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Method Not Allowed")
        
        
    def test_update_actor_with_valid_token_missing_permission_403(self):
        updated_actor_id = Actor.query.all()[0].id
        res = self.client().patch(f'/actors/{updated_actor_id}', json={"age":1}, headers={"Authorization": "Bearer {}".format(self.assistant_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],"Permission not found." )
        
    
    def test_update_actor_with_valid_token_200(self):
        updated_actor = Actor.query.all()[0]
        res = self.client().patch(f'/actors/{updated_actor.id}', json={"age":1}, headers={"Authorization": "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['id'], updated_actor.id)
        self.assertEqual(data['actor']['name'], updated_actor.name)
        self.assertEqual(data['actor']['age'], updated_actor.age)
        self.assertEqual(data['actor']['gender'], updated_actor.gender)

    def test_update_movie_with_valid_token_missing_permission_403(self):
        updated_movie_id = Movie.query.all()[0].id
        res = self.client().patch(f'/movies/{updated_movie_id}', json={"age":1}, headers={"Authorization": "Bearer {}".format(self.assistant_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],"Permission not found." )
        
    def test_update_actor_with_valid_token_200(self):
        updated_movie = Movie.query.all()[0]
        res = self.client().patch(f'/movies/{updated_movie.id}', json={"title":'This is a new title..'}, headers={"Authorization": "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['id'], updated_movie.id)
        self.assertEqual(data['movie']['title'], updated_movie.title)

    
    def test_create_new_movie_without_token_401(self):
        
        movies_len_before_request = len(Movie.query.all())
        res = self.client().post('/movies', json={"title":"test title", "release_date":"30/11/2020"})
        data = json.loads(res.data)
        movies_len_after_request = len(Movie.query.all())
        
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Authorization header is expected.")
        self.assertEqual(movies_len_before_request,movies_len_after_request)  
          

    def test_create_new_movie_missing_param_400(self):
        movies_len_before_request = len(Movie.query.all())
        res = self.client().post('/movies', json={"title":"test title"}, headers={"Authorization": "Bearer {}".format(self.producer_token)},)
        data = json.loads(res.data)
        movies_len_after_request = len(Movie.query.all())
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(movies_len_before_request,movies_len_after_request) 
        
    def test_create_new_movie_200(self):
        movies_len_before_request = len(Movie.query.all())
        res = self.client().post('/movies', json={"title":"test title", "release_date":"30/11/2020"}, headers={"Authorization": "Bearer {}".format(self.producer_token)},)
        data = json.loads(res.data)
        movies_len_after_request = len(Movie.query.all())
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], "test title")
        self.assertNotEqual(movies_len_before_request,movies_len_after_request) 
        
        
    def test_create_new_actor_without_token_401(self):
        actor_len_before_request = len(Actor.query.all())
        res = self.client().post('/actors', json={"name":"test", "age":12, "gender":"Male"})
        data = json.loads(res.data)
        actor_len_after_request = len(Actor.query.all())
        
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Authorization header is expected.")
        self.assertEqual(actor_len_before_request,actor_len_after_request)
        
    def test_create_new_actor_missing_param_400(self):
        actor_len_before_request = len(Actor.query.all())
        res = self.client().post('/actors', json={"name":"won't work"}, headers={"Authorization": "Bearer {}".format(self.producer_token)},)
        data = json.loads(res.data)
        actor_len_after_request = len(Actor.query.all())
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(actor_len_after_request,actor_len_before_request)

    def test_create_new_actor_200(self):
        actor_len_before_request = len(Actor.query.all())
        res = self.client().post('/actors', json={"name":"it worked", "age":123, "gender":"Male"}, headers={"Authorization": "Bearer {}".format(self.producer_token)},)
        data = json.loads(res.data)
        actor_len_after_request = len(Movie.query.all())
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['new_actor']['name'], "it worked")
        self.assertEqual(data['new_actor']['name'], "it worked")
        self.assertEqual(data['new_actor']['age'], 123)
        self.assertEqual(data['new_actor']['gender'], "Male")
        self.assertNotEqual(actor_len_before_request,actor_len_after_request) 
    
    def test_delete_actor_with_valid_token(self):
        
        deleted_actor_id = Actor.query.all()[0].id
        res = self.client().delete(f'/actors/{deleted_actor_id}',  headers={"Authorization": "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_actor'],deleted_actor_id )
        
    def test_delete_non_exsisting_actor_with_valid_token(self):
      
        res = self.client().delete('/actors/42342343',  headers={"Authorization": "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_delete_exsisting_actor_without_token(self):
        res = self.client().delete('/actors/1',  headers={"Authorization": "Bearer "})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_non_exsisting_movie_with_valid_token(self):
     
      
        res = self.client().delete('/movies/42342343',  headers={"Authorization": "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_delete_exsisting_movie_without_token(self):
        res = self.client().delete('/movies/1',  headers={"Authorization": "Bearer "})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
        
    def test_delete_movie_with_valid_token(self): 
        deleted_movie_id = Movie.query.all()[0].id
        res = self.client().delete(f'/movies/{deleted_movie_id}',  headers={"Authorization": "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_movie'],deleted_movie_id )
        
   


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

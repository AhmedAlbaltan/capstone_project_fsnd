'''

'''
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import datetime
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
        
    app = Flask(__name__)
    setup_db(app)
    CORS(app,  resources={r"/*": {"origins": "*"}}) 
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
        
        return response

    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''

    ## ROUTES

    @app.route('/')
    def index():
        return jsonify({
            'success':True,
            "msg":"it worked, YAY!"
        })


    @app.route('/actors')
    @requires_auth(permission='view:actor')
    def get_actors(payload):
        actors = [actor.to_dict() for actor in Actor.query.all()]
        
        return jsonify({
            'success':True,
            'actors':actors
        }),200
        
        
    @app.route('/movies')
    @requires_auth(permission='view:movie')
    def get_movies(payload):
        movies = [movie.to_dict() for movie in Movie.query.all()]
        
        return jsonify({
            'success':True,
            'movies':movies
        }),200
        
        
    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='add:actor')
    def create_actor(payload):
        body = request.get_json()
        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400)
        try:
            actor = Actor(name=body['name'], age=body['age'], gender=body['gender'])
            actor.insert()
            return jsonify({
                'success':True,
                'new_actor':actor.to_dict()
            }),200
        except:
            abort(500)
        
        
    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='add:movie')
    def create_movie(payload):
        body = request.get_json()
        if 'title' not in body or 'release_date' not in body:
            abort(400)
        try:
            date_str = body['release_date']
            format_str = '%d/%m/%Y'
            datetime_obj = datetime.datetime.strptime(date_str, format_str)
            movie = Movie(title=body['title'], release_date=datetime_obj)
            movie.insert()
            return jsonify({
                'success':True,
                'movie':movie.to_dict()
            }),200
        except:
            abort(500)


    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='remove:actor')
    def remove_actor(payload, id):
        actor = Actor.query.get(id)
        
        if actor is None :
            abort(404)
        try:
            actor.delete()
            return jsonify({
                 'success':True,
                'deleted_actor':id
             })
        except:
            abort(500)
            
        
        
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('remove:movie')
    def remove_movie(payload, id):
        movie = Movie.query.get(id)
        
        if movie:
            try:
                movie.delete()
                return jsonify({
                    'success':True,
                    'deleted_movie':id
                })
            except:
                
                abort(500)
        else:
            abort(404)
        

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='modify:actor')
    def update_actor(payload, id):
        actor = Actor.query.get(id)
        
        if actor:
            body = request.get_json()
            try:
                actor.name = body['name'] if 'name' in body else actor.name
                actor.age = body['age'] if 'age' in body else actor.age
                actor.gender = body['gender'] if 'gender' in body else actor.gender
                actor.update()
                return jsonify({
                    'success':True,
                    'actor':actor.to_dict() #can be drink.long too
                })
            except:
                abort(500)
        else:
            abort(404)
        
        
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='modify:movie')
    def update_movie(payload, id):
        movie = Movie.query.get(id)
        
        if movie:
            body = request.get_json()
            try:
                movie.title = body['title'] if 'title' in body else movie.title
                movie.release_date = body['release_date'] if 'release_date' in body else movie.release_date
                movie.update()
                return jsonify({
                    'success':True,
                    'movie':movie.to_dict() #can be drink.long too
                })
            except:
                abort(500)
        else:
            abort(404)
        


        

        

    ## Error Handling


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed'
        }), 405 
        
    @app.errorhandler(400)
    def badrequest(error):
        return jsonify({
                        "success": False, 
                        "error": 400,
                        "message": "bad request"
                        }), 400
        
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "unprocessable"
                        }), 422


    @app.errorhandler(404)
    def resource_not_found(error):
        
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404
        

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success':False,
            'error':500,
            'message':'Inernal Server Error'
        }),500
        
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unathorized'
        }), 401


    @app.errorhandler(AuthError)
    def authError(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error.get('description')
        }), error.status_code
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

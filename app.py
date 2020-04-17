import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, Casting, db
import datetime
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Actor endpoints

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        """ Returns status code 200 and json 
        {"success": True, "actors": actors}
        where actors is the list of actors
        or appropriate status code indicating 
        reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        """
        try:
            actors = [actor.format() for actor in Actor.query.all()]
            return jsonify({"success": True, "actors": actors}), 200
        except Exception:
            abort(404)
        finally:
            db.session.close()

    @app.route('/actors/<int:id>/movies')
    @requires_auth('get:actors')
    def get_actor_movies(jwt, id):
        """ Returns status code 200 and json 
        {"success": True, "actor_id": id, 
        "actor": actor_name, "movies": movies_list}
        or appropriate status code indicating reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        id -- actor id
        """
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                raise
            movies_id_list = actor.format_long()['movies']
            movies_title_tuple_list = db.session.query(Movie.title).filter(
                Movie.id.in_(movies_id_list)).all()
            movies_title_list = [
                item for sublist in movies_title_tuple_list for item in sublist]

            return jsonify({
                "success": True,
                "actor_id": id,
                "actor": actor.format()['name'],
                "movies": movies_title_list}), 200
        except Exception:
            abort(404)
        finally:
            db.session.close()

    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actors')
    def create_actor(jwt):
        """ Returns status code 200 and json 
        {"success": True, "actor": actor}
        where actor is the newly created actor in json format
        or appropriate status code indicating reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        """
        data = request.get_json()
        try:
            if 'name' not in data.keys() or 'age' not in data.keys() or 'gender' not in data.keys():
                raise
            actor = Actor(name=data['name'],
                          age=data['age'], gender=data['gender'])
            actor.insert()
            return jsonify({"success": True, "actor": actor.format()}), 200
        except Exception:
            abort(400)
        finally:
            db.session.close()

    @app.route('/actors/<int:id>', methods=["PATCH"])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        """ Returns status code 200 and json 
        {"success": True, "actor": actor}
        where actor is the updated actor in json format
        or appropriate status code indicating reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        id -- actor id to patch
        """
        data = request.get_json()
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                raise
            if 'name' in data.keys():
                actor.name = data['name']
            if 'age' in data.keys():
                actor.age = data['age']
            if 'gender' in data.keys():
                actor.gender = data['gender']
            actor.update()
            return jsonify({"success": True, "actor": actor.format()}), 200
        except Exception:
            abort(404)
        finally:
            db.session.close()

    @app.route('/actors/<int:id>', methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        """ Returns status code 200 and json 
        {"success": True, "deleted_id": deleted actor_id}
        where id is the deleted actor id
        or appropriate status code indicating 
        reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        id -- actor id to delete
        """
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                raise
            actor.delete()
            return jsonify({"success": True, "deleted_id": id}), 200
        except Exception:
            abort(404)
        finally:
            db.session.close()

    # Movie endpoints

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        """ Returns status code 200 and json 
        {"success": True, "movies": movies}
        where movies is the list of movies
        or appropriate status code indicating 
        reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        """
        try:
            movies = [movie.format() for movie in Movie.query.all()]
            return jsonify({"success": True, "movies": movies}), 200
        except Exception:
            abort(404)
        finally:
            db.session.close()

    @app.route('/movies/<int:id>/actors')
    @requires_auth('get:movies')
    def get_movie_actors(jwt, id):
        """ Returns status code 200 and json 
         {"success": True, "movie_id": id, 
        "movie": movie_title, "actors": cast actors_list} 
        or appropriate status code indicating 
        reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        id -- movie id
        """
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                raise
            actors_id_list = movie.format_long()['actors']
            actors_name_tuple_list = db.session.query(Actor.name).filter(
                Actor.id.in_(actors_id_list)).all()
            actors_name_list = [
                item for sublist in actors_name_tuple_list for item in sublist]

            return jsonify({
                "success": True,
                "movie_id": id,
                "movie": movie.format()['title'],
                "actors": actors_name_list}), 200
        except Exception:
            abort(404)
        finally:
            db.session.close()

    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movies')
    def create_movie(jwt):
        """ Returns status code 200 and json 
        {"success": True, "movie": movie}
        where movie is the newly created movie in json format
        or appropriate status code indicating reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        """
        data = request.get_json()
        try:
            if 'title' not in data.keys() or 'release_date' not in data.keys():
                raise
            movie = Movie(title=data['title'],
                          release_date=data['release_date'])
            movie.insert()
            return jsonify({"success": True, "movie": movie.format()}), 200
        except Exception:
            abort(400)
        finally:
            db.session.close()

    @app.route('/movies/<int:id>', methods=["PATCH"])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        """ Returns status code 200 and json 
        {"success": True, "movie": movie}
        where movie is the updated movie in json format
        or appropriate status code indicating reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        id -- movie id to patch
        """
        data = request.get_json()
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                raise
            if 'title' in data.keys():
                movie.title = data['title']
            if 'release_date' in data.keys():
                movie.release_date = data['release_date']
            movie.update()
            return jsonify({"success": True, "movie": movie.format()}), 200
        except Exception:
            abort(404)
        finally:
            db.session.close()

    @app.route('/movies/<int:id>', methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        """ Returns status code 200 and json 
        {"success": True, "deleted_id": deleted movie_id}
        where id is the deleted movie id
        or appropriate status code indicating 
        reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        id -- movie id to delete
        """
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                raise
            movie.delete()
            return jsonify({"success": True, "deleted_id": id}), 200
        except Exception:
            abort(404)
        finally:
            db.session.close()

    # Casting endpoints

    @app.route('/cast')
    @requires_auth('get:cast')
    def get_cast(jwt):
        """ Returns status code 200 and json 
        {"success": True, "cast": cast_list}
        where cast_list is the association between movies and actors
        or appropriate status code indicating 
        reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        """
        try:
            cast_list = [cast.format() for cast in Casting.query.all()]
            return jsonify({"success": True, "cast": cast_list}), 200
        except Exception:
            abort(500)
        finally:
            db.session.close()

    @app.route('/cast', methods=["POST"])
    @requires_auth('post:cast')
    def create_casting(jwt):
        """ Returns status code 200 and json 
        {"success": True, "cast": cast}
        where cast is the newly created association between movies and actors in json format
        or appropriate status code indicating reason for failure

        Keyword arguments: 
        jwt -- json web token with permission
        """
        data = request.get_json()
        try:
            if 'actor_id' not in data.keys() or 'movie_id' not in data.keys():
                raise
            cast = Casting(actor_id=data['actor_id'],
                           movie_id=data['movie_id'], actor_award=data['actor_award'])
            cast.insert()
            return jsonify({"success": True, "cast": cast.format()}), 200
        except Exception:
            abort(400)
        finally:
            db.session.close()

    # Error Handling

    @app.errorhandler(400)
    def unprocessable(error):
        """ error handling for bad request"""
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """ error handling for entity not found"""
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def not_found(error):
        """ error handling for server error"""
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        """ error handling for AuthError 401 or 403"""
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)   # app.run()

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    """Movie have title and release date"""
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    release_date = Column(Date, nullable=False)
    actors = db.relationship('Casting',
                             backref='movie',
                             lazy=True,
                             collection_class=list,
                             cascade='all, delete')

#  A type for datetime.date() objects.

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%Y-%m-%d')}

    def format_long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%Y-%m-%d'),
            'actors': [actor.format()['actor_id'] for actor in self.actors]}

    def __repr__(self):
        return f'<Movie {self.format()}>'


class Actor(db.Model):
    """Actor have name, age and gender"""
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(120), nullable=False)
    movies = db.relationship('Casting',
                             backref='actor',
                             lazy=True,
                             collection_class=list,
                             cascade='all, delete')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}

    def format_long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.format()['movie_id'] for movie in self.movies]}

    def __repr__(self):
        return f'<Actor {self.format()}>'


class Casting(db.Model):
    __tablename__ = 'Casting'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('Actor.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('Movie.id'), nullable=False)

    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'actor_id': self.actor_id,
            'movie_id': self.movie_id}

    def __repr__(self):
        return f'<Casting {self.format()}>'

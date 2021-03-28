from flask import Flask
from flask_restful import Api, reqparse

from .resources.movie import Movie
from .imdb_reader import IMBDReader


def create_flask_app():
  print("Starting API...")
  app = Flask(__name__)
  api = Api(app)
  imdb_dataset = IMBDReader()
  print("Loading resources...")
  api.add_resource(Movie, "/movie", resource_class_kwargs={"imdb_dataset": imdb_dataset})
  print("Resources Loaded!")
  return app

from flask import Flask
from flask_restful import Api, reqparse

from .resources.movie import Movie


def create_flask_app():
  app = Flask(__name__)
  api = Api(app)
  api.add_resource(Movie, "/movie")
  return app

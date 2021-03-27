from flask import Flask
from flask_restful import Api, reqparse

from .resources.movie import Movie


def main():
  app = Flask(__name__)
  api = Api(app)
  api.add_resource(Movie, "/movie")
  app.run(debug=True)


if __name__ == "__main__":
  main()

from flask import Flask
from flask_restful import Api, reqparse

from resources.movie import Movie


app = Flask(__name__)
api = Api(app)


api.add_resource(Movie, "/movie")


if __name__ == "__main__":
  app.run(debug=True)

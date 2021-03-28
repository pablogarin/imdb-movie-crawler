from flask_restful import Resource


class Movie(Resource):
  def __init__(self, imdb_dataset):
    self.imdb_dataset = imdb_dataset

  def get(self):
    data = self.imdb_dataset.movie_list
    return {"ok": True, "count": len(data), "data": data}

from flask_restful import Resource


class Movie(Resource):
  def __init__(self):
    pass

  def get(self):
    return {"ok": True}

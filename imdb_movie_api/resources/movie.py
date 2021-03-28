from flask_restful import reqparse
from flask_restful import Resource


class Movie(Resource):
    def __init__(self, imdb_dataset):
        self.imdb_dataset = imdb_dataset

    def get(self):
        # Parse query params
        parser = reqparse.RequestParser()
        parser.add_argument("query", type=str, required=False)
        args = parser.parse_args()
        query = args["query"]
        if query:
            results = []
            title_table = self.imdb_dataset.title_table
            year_table = self.imdb_dataset.year_table
            genre_table = self.imdb_dataset.genre_table
            director_table = self.imdb_dataset.director_table
            star_table = self.imdb_dataset.star_table
            sanitized_query = query.lower().strip()
            movies = dict()
            search_params = sanitized_query.split(" ")
            for param in search_params:
                found, node = self.imdb_dataset.search_params.search(param)
                if found:
                    for key in node.keys:
                        if key in director_table:
                            if "directors" not in movies:
                                movies["directors"] = set()
                            movies["directors"] = set.union(
                                movies["directors"],
                                director_table[key])
                        if key in star_table:
                            if "stars" not in movies:
                                movies["stars"] = set()
                            movies["stars"] = set.union(
                                movies["stars"],
                                star_table[key])
                        if key in title_table:
                            if "titles" not in movies:
                                movies["titles"] = set()
                            movies["titles"] = set.union(
                                movies["titles"],
                                title_table[key])
            if len(movies.keys()) > 0:
                results = set.intersection(*movies.values())
            return {"query": query, "results": [dict(movie) for movie in results]}
        else:
            data = self.imdb_dataset.movie_list
            return {"ok": True, "count": len(data), "data": list(map(lambda movie: dict(movie), data))}
    
    def _search_by_director_and_actor(self, query):
        pass

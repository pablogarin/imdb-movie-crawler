from flask_restful import reqparse
from flask_restful import Resource
from functools import lru_cache


class Movie(Resource):
    def __init__(self, imdb_dataset):
        self.imdb_dataset = imdb_dataset

    def get(self):
        # Parse query params
        parser = reqparse.RequestParser()
        parser.add_argument("query", type=str, required=False)
        parser.add_argument("strict", type=bool, required=False)
        args = parser.parse_args()
        query = args["query"]
        strict = args["strict"]
        if query:
            if strict is None:
                strict = False
            sanitized_query = query.lower().strip()
            search_params = set(sanitized_query.split(" "))
            results, match_type = self._search_movie(
                "+".join(search_params),
                strict=strict)
            return {
                "query": query,
                "matched": match_type,
                "count": len(results),
                "results": [dict(movie) for movie in results]
            }
        else:
            data = self.imdb_dataset.movie_list
            return {
                "count": len(data),
                "results": list(map(lambda movie: dict(movie), data))
            }

    @lru_cache
    def _search_movie(self, search_query, strict=False):
        search_params = search_query.split("+")
        results = []
        title_table = self.imdb_dataset.title_table
        genre_table = self.imdb_dataset.genre_table
        director_table = self.imdb_dataset.director_table
        star_table = self.imdb_dataset.star_table
        movies = dict()
        all_found = True
        for param in search_params:
            found, node = self.imdb_dataset.search_params.search(param)
            all_found = all_found and found
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
                    if key in genre_table:
                        if "genres" not in movies:
                            movies["genres"] = set()
                        movies["genres"] = set.union(
                            movies["genres"],
                            genre_table[key])
        match_type = "exact"
        if not all_found:
            match_type = "partial"
        if len(movies.keys()) > 0:
            results = set.intersection(*movies.values())
        if strict and not all_found:
            results = []
        return results, match_type

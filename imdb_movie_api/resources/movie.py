from flask_restful import reqparse
from flask_restful import Resource
from functools import lru_cache

from imdb_movie_api.utils.string import normalize


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
            sanitized_query = normalize(query.lower().strip())
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
        dataset = self.imdb_dataset
        search_params = search_query.split("+")
        results = []
        data_table = dataset.data_table
        matches_found = dict()
        all_found = True
        for param in search_params:
            movies = set()
            found, node = dataset.search_params.search(param)
            all_found = all_found and found
            if node is not None:
                possible_results = dataset.search_params.autocomplete_word(
                    param,
                    node)
                for (word, sub_node) in possible_results:
                    for key in sub_node.keys:
                        data = set()
                        if key in data_table:
                            data = data_table[key]
                        movies = set.union(movies, data)
            if len(movies) > 0:
                matches_found[param] = movies
        match_type = "exact"
        if not all_found:
            match_type = "partial"
        if len(matches_found.keys()) > 0:
            results = set.intersection(*matches_found.values())
        return results, match_type

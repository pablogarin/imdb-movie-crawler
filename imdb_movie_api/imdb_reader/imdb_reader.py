from lxml import html
import requests
import re

from imdb_movie_api.trie import Trie
from imdb_movie_api.imdb_reader.movie import Movie
from imdb_movie_api.utils.string import normalize


class IMBDReader(object):
    url = "https://www.imdb.com/search/title/"\
        "?groups=top_1000&sort=user_rating,desc&count=%s&start=%s"
    movie_list = []
    data_table = {}
    search_params = Trie()
    indexes = [
        "title",
        "director",
        "stars",
        "genres",
        "year"
    ]
    MAX_PAGES = 10

    def __init__(self):
        print("Fetching movie information...")
        self.movie_list = []
        # Fetch all movies and parse them
        for page in range(self.MAX_PAGES):
            start = 0
            if page > 0:
                start = 100*page+1
            self.movie_list += self._get_movies(start)
        # Index all results for quick lookups
        for movie in self.movie_list:
            dict_movie = dict(movie)
            for index in self.indexes:
                if index not in dict_movie:
                    continue
                keyword = dict_movie[index]
                if type(keyword) == str:
                    self._setup_keyword(keyword, movie)
                elif type(keyword) == list:
                    for kw in keyword:
                        self._setup_keyword(kw, movie)
        print("Movies dataset loaded.")

    def _setup_keyword(self, keyword, movie):
        # If the keyword is not in the lookup table, add it
        if keyword not in self.data_table:
            self.data_table[keyword] = set()
        self.data_table[keyword].add(movie)
        # add each word to the Trie data structure
        for word in keyword.strip().lower().split(" "):
            final_node = self.search_params.add(normalize(word))
            if final_node is not None:
                """ If we reached the final node, add the
                full keyword in the node key set in order
                to match it with the lookup table"""
                final_node.keys.add(keyword)

    def _get_movies(self, start=0, count=100):
        try:
            response = requests.get(self.url % (count, start))
            if response.status_code >= 200 and response.status_code < 400:
                page_content = html.fromstring(response.text)
                movie_tiles = page_content.find_class("lister-item")
                return list(
                    map(self._movie_dict_from_html, movie_tiles)
                )
            else:
                raise Exception("Couldn't connecto to server.")
        except Exception as e:
            print("Couldn't fetch movie data. Reason: '%s'" % e)

    def _extract_text_from_cssselector(self, dom, selector, index=0):
        try:
            return str(dom.cssselect(selector)[index].text_content())
        except Exception as e:
            print(
                "Can't extract text from %s using the selector '%s'."
                "Check the selector." % (dom, selector))
            print("Details: '%s" % e)
            return None

    def _get_director(self, string):
        regexp = r"Director:([^\|]+)"
        m = re.search(regexp, string)
        if m:
            director = m.groups()[0]
            return director.strip()
        return ""

    def _get_stars(self, string):
        regexp = r"Stars:(.*)"
        m = re.search(regexp, string)
        if m:
            stars = m.groups()[0]
            return stars.strip().split(", ")
        return ""

    def _movie_dict_from_html(self, data):
        title = self._extract_text_from_cssselector(
            data, ".lister-item-header a")

        year = self._extract_text_from_cssselector(
            data, ".lister-item-year")

        people_involved = self._extract_text_from_cssselector(
            data, "p:contains(Director)").replace("\n", "")

        director = self._get_director(people_involved)
        stars = self._get_stars(people_involved)

        genres = self._extract_text_from_cssselector(
            data, ".genre"
        ).strip().split(", ")

        return Movie(
            title,
            re.sub(r"[^0-9]", "", year),
            director,
            stars,
            genres)

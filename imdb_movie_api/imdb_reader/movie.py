class Movie(object):
    _title = None
    _year = None
    _director = None
    _stars = None
    _genres = None

    def __init__(self, title, year, director, stars, genres):
        self.title = title
        self.year = year
        self.director = director
        self.stars = stars
        self.genres = genres

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, value):
        self._director = value

    @property
    def stars(self):
        return self._stars

    @stars.setter
    def stars(self, value):
        self._stars = value

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, value):
        self._genres = value

    def __repr__(self):
        return str(dict(self))

    # Entry set used to map to dict
    def __iter__(self):
        d = {
            "title": self._title,
            "year": self._year,
            "director": self._director,
            "stars": self._stars,
            "genres": self._genres
        }
        for key in d.keys():
            yield (key, d[key])

class Movie(object):
    _title = None
    _year = None
    _director = None
    _stars = None
    _genre = None

    def __init__(self, title, year, director, stars, genre):
        self.title = title
        self.year = year
        self.director = director
        self.stars = stars
        self.genre = genre

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
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    def __repr__(self):
        return str(dict(self))

    # Entry set used to map to dict
    def __iter__(self):
        d = {
            "title": self._title,
            "year": self._year,
            "director": self._director,
            "stars": self._stars
        }
        for key in d.keys():
            yield (key, d[key])

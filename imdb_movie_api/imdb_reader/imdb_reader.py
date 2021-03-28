from lxml import html
import requests
import re


class IMBDReader(object):
  url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=%s&start=%s"
  movie_list = []

  def __init__(self):
    print("Fetching movie information...")
    self.movie_list = []
    for page in range(2):
      start = 0
      if page > 0:
        start = 100*page+1
      self.movie_list += self._get_movies(start)
    print("Movies dataset loaded.")

  def _get_movies(self, start=0, count=100):
    response = requests.get(self.url % (count, start))
    if response.status_code >= 200 and response.status_code < 400:
      page_content = html.fromstring(response.text)
      movie_tiles = page_content.find_class("lister-item")
      return list(
        map(self._movie_dict_from_html, movie_tiles)
      )
    else:
      raise Exception("Couldn't connecto to server.")
  
  def _extract_text_from_cssselector(self, dom, selector, index=0):
    try:
      return str(dom.cssselect(selector)[index].text_content())
    except:
      print(
        "Can't extract text from %s using the selector '%s'. Check the selector." %
        (dom, selector)
      )
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
    title = self._extract_text_from_cssselector(data, '.lister-item-header a')
    year = self._extract_text_from_cssselector(data, '.lister-item-year')
    people_involved = self._extract_text_from_cssselector(data, 'p:contains(Director)')\
      .replace("\n", "")
    director = self._get_director(people_involved)
    stars = self._get_stars(people_involved)
    return {
      "title": title,
      "year": re.sub(r"[^0-9]", "", year),
      "director": director,
      "stars": stars
    }
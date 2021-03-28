# IMDB Movie API

API to find movies by title, director, stars or genre.

## Usage

### GET /movie

Returns the complete movie list. This list is comprised of the top 1000 movies of all time (https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=1000&start=0)

#### Query Params:
- query: A string with the search. This can be any of the listed fields

#### Response:
This endpoint responds with a JSON containing the following elements:
- count: The total number of matches. If no query is given, it should show the total number of movies in the list (in this case, 1000).
- results: A list with the information of each movie. Each movie has: title, year, director, stars, genre.
- query: Only returned if a query is given. Same as the search query.
- matched: Only returned if a query is given. Indicates if the query was an `exact` or `partial` match.
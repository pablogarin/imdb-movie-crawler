# IMDB Movie API

API to find movies by title, director, stars or genre.

## Build

In order to run the API, you have two options: localy and in a container.

### Running API localy

In a UNIX base OS\*, open a terminal and execute the following command:

`sudo python3 setup.py install`

Once the python package finishes installing, you'll have a new command called `start-app` in your terminal. Whenever you call it it'll start a development server running the app.

\*NOTE: If you have a windows machine, see the section *Running in a container*.

### Running in a container

If you want to run this app in an OS agnostic way, either because you have a DOS Based OS, you want to run it on a Kubernetes Cluster, or you don't want to install the python package, then you'll need to run the app as a container. In order to do this, you'll need to have Docker installed in your system \([How to install Docker](https://docs.docker.com/get-docker/)\). If you already have docker, run the following command to build the image:

`docker build . -t imdb_movie_api`

If the build ends without error, start up the container with this command:

`docker run -d -p3000:3000 --name imbd_movie_api-container imdb_movie_api`

*Explanation*:
- `docker run`: starts a container.
- `-d`: Run in 'detached' mode (background).
- `-p3000:3000`: maps the local port 3000 to the container's 3000 port.
- `--name [NAME_OF_CONTAINER]`: gives the container a name, in this case `imbd_movie_api-container`, but you can choose any name. It's helpful to give it name in order to stop it without having to reference it's hash ID.
- `imdb_movie_api`: the tag of the image we created in the precious step. If you tagged the image with a different name, make sure to pass it here.

Finaly, when we are no longer using the container, we can stop it running this command:

`docker stop imbd_movie_api-container`

NOTE: If you changed the container name, make sure to pass it here.

## Usage

The base URL for the API is http://localhost:3000, and you can access it anyway you want, (eg: Postman, curl, browser, etc).

### GET /movie

Returns the complete movie list. This list is comprised of the top 1000 movies of all time: [IMDB Top 1000 movies](https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=0)

#### Query Params:
- query: A string with the search. This can be any of the listed fields

#### Response:
This endpoint responds with a JSON containing the following elements:
- `count`: The total number of matches. If no query is given, it should show the total number of movies in the list (in this case, 1000).
- `results`: A list with the information of each movie. Each movie has: title, year, director, stars, genre.
- `query`: Only returned if a query is given. Same as the search query.
- `matched`: Only returned if a query is given. Indicates if the query was an `exact` or `partial` match. This means that all the given words were found in the movie list.

Example:
`curl -X GET "http://localhost:3000/movie?query=hanks+spielberg"`
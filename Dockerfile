FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY imdb_movie_api ./imdb_movie_api

RUN python -m pip install -r requirements.txt

CMD ["gunicorn", "-w1", "-b0.0.0.0:3000", "imdb_movie_api:app"]
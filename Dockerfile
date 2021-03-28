FROM python:3-alpine

WORKDIR /app

COPY setup.py ./
COPY imdb_movie_api ./imdb_movie_api

RUN python setup.py install

RUN python -m pip install gunicorn

CMD ["gunicorn", "-w1", "-b0.0.0.0:3000", "imdb_movie_api:app"]
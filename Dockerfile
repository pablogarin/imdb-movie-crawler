FROM python:3-alpine

WORKDIR /app

COPY app setup.py ./

RUN python setup.py install

CMD ["start-app"]
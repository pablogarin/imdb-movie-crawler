from imdb_movie_api import create_flask_app


def main():
  app = create_flask_app()
  app.run()


if __name__ == "__main__":
  main()
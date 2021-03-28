from .main import create_flask_app


app = create_flask_app()


def main():
  app.run()

from .main import create_flask_app


print("name", __name__)
app = create_flask_app()


def main():
    app.run(host='0.0.0.0', port=3000)

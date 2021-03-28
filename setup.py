from setuptools import find_packages
from setuptools import setup


setup(
    name="IMBD Movie Crawler",
    version="1.0.0",
    description="Movie crawler and API.",
    author="Pablo Garin",
    author_email="pablo.garin@hotmail.com",
    url="https://github.com/pablogarin/imdb-movie-crawler",
    packages=find_packages(),
    install_requires=[
        "Flask>=1.1.2",
        "Flask-RESTful",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "start-app = main:main"
        ]
    }
)
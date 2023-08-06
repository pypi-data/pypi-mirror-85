import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="py-echo",
    version="1.0.2",
    description="stylize prints with colors, backgrounds, and styles",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/murad-sinatra/",
    author="Murad Sinatra",
    author_email="muradmorshedd@gmail.com",
    py_modules=['echo'],
)

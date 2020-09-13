#!/usr/bin/env python
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask
from flask_restplus import Resource, Api
app = Flask("suggest_api")


@app.route('/')
def hello_world():
    return 'Hello, Emma!'

if __name__ == "__main__":
    app.run(host="localhost", debug=True)
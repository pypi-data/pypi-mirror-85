#!/usr/bin/env python
import os

from flask import Flask
from flask_desktop_ui import FlaskDesktopUI

from jamd import markdown_parser


app = Flask(__name__, static_url_path='')


def run(path):
    app.static_folder = os.path.dirname(os.path.abspath(path))
    markdown_contents = ''

    if os.path.exists(path):
        with open(path) as file:
            markdown_contents = file.read()

    @app.route('/')
    def markdown_in_html_endpoint():
        return markdown_parser.to_html(markdown_contents)

    FlaskDesktopUI(app).run()

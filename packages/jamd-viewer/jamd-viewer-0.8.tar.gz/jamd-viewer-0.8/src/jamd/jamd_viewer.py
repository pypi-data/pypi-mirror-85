#!/usr/bin/env python
import os

from flask import Flask
from flask_desktop_ui import FlaskDesktopUI

from jamd import markdown_parser, shell
from jamd.github_markdown_template import GithubMarkdownTemplate


class Styles:
    GITHUB = 'github'


STYLE_TEMPLATE = {
    Styles.GITHUB: GithubMarkdownTemplate
}


app = Flask(__name__, static_url_path='')
markdown_contents = ''
template = None


@app.route('/')
def markdown_in_html_endpoint():
    return markdown_parser.to_html(markdown_contents, template=template)


def run(path, style=None):
    global markdown_contents
    global template

    if not shell.file_exists(path):
        markdown_contents = 'File `{path}` does not exist'.format(path=path)
        template = _style_template(style)
        FlaskDesktopUI(app).run()
        return

    app.static_folder = os.path.dirname(os.path.abspath(path))
    markdown_contents = shell.read_file(path)
    template = _style_template(style)
    FlaskDesktopUI(app).run()


def _style_template(style):
    return STYLE_TEMPLATE[style] if style in STYLE_TEMPLATE else None

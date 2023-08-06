import markdown


def to_html(markdown_text, template=None):
    content = markdown.markdown(markdown_text, extensions=['extra'])

    if template is None:
        return content

    return template(content).html

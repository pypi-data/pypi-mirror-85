import markdown


def to_html(markdown_text):
    return markdown.markdown(markdown_text, extensions=['extra'])

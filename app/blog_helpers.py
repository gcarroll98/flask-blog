from markdown import markdown
import os

def render_markdown(file_name, dir_path = 'app/templates'):
    html = ""
    path = os.path.join(dir_path, file_name)
    with open(path) as html_file:
        html = html_file.read()
        html = markdown(html)
    return html
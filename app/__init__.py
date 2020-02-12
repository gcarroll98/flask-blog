import os
import sqlite3
from flask import (Flask, request, session, g, redirect, url_for, abort, render_template, flash)


app = Flask(__name__)
app.config.from_object(__name__)
# Set the secret key to some random bytes. Keep this really secret!

app.config.update(
    DATABASE = os.path.join(app.root_path, 'app.db'),
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/',
    USERNAME='admin',
    PASSWORD='default'
)

from app import routes

from app import app
from markdown import markdown
from flask import render_template_string, request, session
from app.helpers import render_markdown
from os import listdir
from os.path import isfile,join

import flask

#home page 
@app.route("/")
def home():
    return render_markdown('index.md')

#login with POST
@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        session['user_name'] = request.values['user_name']
    return ""

#generic page
@app.route("/<view_name>")

#new template
def render_page (view_name):
    html = render_markdown (view_name +'.md')
    view_data = {}
    return render_template_string (html, view_name = session)

@app.route("/all")
def all():
    onlyfiles = [f for f in listdir('app/views') if isfile(join('app/views', f))]]
    return onlyfiles
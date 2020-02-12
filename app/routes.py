#import certain functions into the global
#namespace
from app import app
from markdown import markdown
from flask import (render_template, render_template_string, request, session, flash, redirect, abort,g, url_for)
from flask_bootstrap import Bootstrap
from app.blog_helpers import render_markdown
from os import listdir
from os.path import isfile, join, splitext
import flask



#home page
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/all')
def all():
    #TODO: figure out how to find all files 
    #in the app
    view_data = {}
    view_data['pages']= listdir("app\\templates")
    allsplit(view_data)
    return render_template("all.html", data = view_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
    else:
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

def allsplit(view_data):
    i = 0
    while i < len(view_data['pages']):
        temp = {}
        temp = splitext(view_data['pages'][i])
        view_data['pages'][i] = temp[0]
        i+=1
    return view_data

@app.route("/favicon.ico")
def favicon():
    return ""

@app.route("/edit")
def edit():
    return render_template("edit.html")

@app.route("/click_tracker", methods=['GET', 'POST'])
def click_tracker():
    view_data = {}
    view_data["click_count"] = 0
    if request.method == 'POST':
        view_data["click_count"] = request.values["click_count"]
        view_data["click_count"] = int(view_data["click_count"]) + 1
    return render_template('click_tracker.html', data=view_data)
    
@app.route("/user")
def user():
    return render_template("user.html")

#generic page
@app.route("/<view_name>")

#input parameter name must match route parameter
def render_page(view_name):
    return ""


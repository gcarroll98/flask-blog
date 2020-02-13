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
import sqlite3


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
        if request.form['username'] != "admin":
            error = 'Invalid username'
        elif request.form['password'] != "default":
            error = 'Invalid password'
        else:
          session['logged_in'] = True
          flash('You were logged in')
          return redirect(url_for('logout'))

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return render_template('show_entries.html')
    
    
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
    return render_template(view_name + '.hmtl')

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factor = sqlite3.Row 
    return rv

def init_db():
    db = get_db()

    with app.open_resource('schema.sql',mode = 'r') as f:
        db.cursor().executescript(f.read())

    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print ('Initialized the databse.')


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/add', methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title,text) values (?,?)',
            [request.form['title'],request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
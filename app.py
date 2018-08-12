from flask import Flask
from flask import jsonify,request,render_template
from flask_cors import CORS
import csv
import sqlite3
import os

DEFAULT_PATH = os.path.join(os.path.dirname(__file__),'database.sqlite3')

def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

def get_unique_movie_titles():
    data=[]
    con=db_connect()
    cur = con.cursor()
    titles_sql="select distinct title from movie;"
    cur.execute(titles_sql)
    rows = cur.fetchall()
    for item in rows:
      data.append(item[0])
    return data

def get_titles():
  data_set={"data":None}
  unique_movies=get_unique_movie_titles()
  d=[]
  for title in unique_movies:
    d.append({"mtitle":title,"mlink":title})
  data_set["data"]=d
  return data_set

def get_placeids(title):
  data=[]
  placeids_sql="select placeid from movie where title='"+title+"';"
  con=db_connect()
  cur = con.cursor()
  cur.execute(placeids_sql)
  rows = cur.fetchall()
  for item in rows:
    if item[0]=="None" or item[0]=="":
      continue
    else:
      data.append(item[0])
  return data

app = Flask(__name__)
CORS(app)
@app.route('/')
@app.route('/index')
def index():
  return render_template('filter.html')

@app.route('/titles')
def title():
  d=get_titles()
  return jsonify(d)

@app.route('/placeIds')
def place_ids():
  title=request.args.get('title')
  d=get_placeids(title)
  return jsonify(d)

@app.route('/map')
def map():
  title=request.args.get('title')
  return render_template('map.html',title=title)

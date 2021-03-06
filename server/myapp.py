import MySQLdb
from flask import Flask, g, request, jsonify
app = Flask(__name__)
app.debug = True
from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)
@app.before_request
def before_request():
  g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                           MYSQL_DB, port=int(MYSQL_PORT))

@app.teardown_request
def teardown_request(exception):
  if hasattr(g, 'db'): g.db.close()

@app.route('/')
def hello():
  return "Hello, world! - Flask"

@app.route('/login', methods=['POST'])
def login():
  c = g.db.cursor()
  c.execute("SELECT * FROM users WHERE id=%s AND pw=%s", (request.form['id'], request.form['pw']))
  u = list(c.fetchall())
  if len(u) > 0:
      return jsonify({'status':'success', 'msg':'login success'})
  return jsonify({'status':'fail', 'msg':'id not exit or pw error'})

@app.route('/register', methods=['POST'])
def register():
  re = {}
  c = g.db.cursor()
  c.execute("SELECT * FROM users WHERE id=%s", (request.form['id']))
  u = list(c.fetchall())
  if len(u) > 0:
      return jsonify({'status':'fail', 'msg':'id exit'})
  c.execute("INSERT INTO users(id,pw) VALUES(%s,%s)", (request.form['id'], request.form['pw']))
  return jsonify({'status':'success', 'msg':'register success'})
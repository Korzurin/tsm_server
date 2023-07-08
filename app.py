import json
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__) 

@app.route("/")
def index():
	return "soem"

@app.route("/alive_users_coordinates", methods=["GET"])
def get_alive_coordinates():
	conn = psycopg2.connect("dbname=tsm user=postgres")
	cur = conn.cursor()
#	cur.execute("select * from users u where u.status = 'alive' or u.status = 'жив'")
	cur.execute("SELECT *  FROM users s1 WHERE sended_time = (SELECT MAX(sended_time) FROM users s2 WHERE s1.name = s2.name) and (status = 'alive' or status = 'жив')  ORDER BY name;")
	#cur.execute("SELECT *  FROM users s1 WHERE sended_time = (SELECT MAX(sended_time) FROM users s2 WHERE s1.name = s2.name) and (status = 'alive' or status = 'жив') and (color = 'green')  ORDER BY name;")
	results = []
	columns = ("name", "lon", "lat", "color", "status")
	for row in cur.fetchall():
		results.append(dict(zip(columns, row)))

	return jsonify(results)

@app.route("/alive_users_coordinates1", methods=["GET"])
def get_alive_coordinates1():
	conn = psycopg2.connect("dbname=tsm user=postgres")
	cur = conn.cursor()
#	cur.execute("select * from users u where u.status = 'alive' or u.status = 'жив'")
	cur.execute("SELECT *  FROM users s1 WHERE sended_time = (SELECT MAX(sended_time) FROM users s2 WHERE s1.name = s2.name) and (status = 'alive' or status = 'жив') and (color = 'green') ORDER BY name;")
	#cur.execute("SELECT *  FROM users s1 WHERE sended_time = (SELECT MAX(sended_time) FROM users s2 WHERE s1.name = s2.name) and (status = 'alive' or status = 'жив') and (color = 'green')  ORDER BY name;")
	results = []
	columns = ("name", "lon", "lat", "color", "status")
	for row in cur.fetchall():
		results.append(dict(zip(columns, row)))

	return jsonify(results)

@app.route("/alive_users_coordinates_and_order", methods=["GET"])
def get_alive_coordinates_and_order():
	conn = psycopg2.connect("dbname=tsm user=postgres")
	cur = conn.cursor()
#	cur.execute("select * from users u where u.status = 'alive' or u.status = 'жив'")
	cur.execute("SELECT *  FROM users s1 WHERE sended_time = (SELECT MAX(sended_time) FROM users s2 WHERE s1.name = s2.name) and (status = 'alive' or status = 'жив') union select * from pointer_and_order p1 WHERE sended_time = (SELECT MAX(sended_time) FROM pointer_and_order p2 WHERE p1.name = p2.name) and (status = 'alive' or status = 'жив') order by name;")
	results = []
	columns = ("name", "lon", "lat", "color", "status")
	for row in cur.fetchall():
		results.append(dict(zip(columns, row)))

	return jsonify(results)

@app.route("/users_coordinates", methods=["GET"])
def get_coordinates():
	conn = psycopg2.connect("dbname=tsm user=postgres")
	cur = conn.cursor()
#	cur.execute("select * from users")
	cur.execute("SELECT *  FROM users s1 WHERE sended_time = (SELECT MAX(sended_time) FROM users s2 WHERE s1.name = s2.name) and (color = 'green') ORDER BY name;")
	results = []
	columns = ("name", "lon", "lat", "color", "status")
	for row in cur.fetchall():
		results.append(dict(zip(columns, row)))

	return jsonify(results)

@app.route("/users_coordinates", methods=["POST"])
def add_coordinates():
	conn = psycopg2.connect("dbname=tsm user=postgres")
	#cur = conn.cursor()
	print(request)
	user = json.loads(request.data)
	
#	SQL = "insert into users (name, lon, lat, color) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "');"
#	SQL = "insert into users (name, lon, lat, color, sended_time) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "', now()::timestamp);"
	SQL = "insert into users (name, lon, lat, color, status, sended_time) values ('" + str(user["name"]) + "', " + str(user["lon"]) + ", " + str(user["lat"]) + ", '" + str(user["color"]) + "', '" + str(user["status"]) + "', now()::timestamp);"
#	SQL = "insert into users (name, lon, lat, color, status, sended_time) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "', '" + user["status"] + "', now()::timestamp);"
	with conn.cursor() as curs:
    		curs.execute(SQL)
	conn.commit()
	
	#print("insert into users (name, lon, lat, color) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "')")
#	cur.execute("insert into users (name, lon, lat, color) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "');")
	#cur.commit()
	#print(cur.statusmessage)
	return jsonify(user), 201

@app.route("/orders", methods=["POST"])
def add_coordinates_orders():
	conn = psycopg2.connect("dbname=tsm user=postgres")
	#cur = conn.cursor()
	print(request)
	user = json.loads(request.data)
	
#	SQL = "insert into users (name, lon, lat, color) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "');"
#	SQL = "insert into users (name, lon, lat, color, sended_time) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "', now()::timestamp);"
	SQL = "insert into pointer_and_order (name, lon, lat, color, status, sended_time) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "', '" + user["status"] + "', now()::timestamp);"
#	SQL = "insert into users (name, lon, lat, color, status, sended_time) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "', '" + user["status"] + "', now()::timestamp);"
	with conn.cursor() as curs:
    		curs.execute(SQL)
	conn.commit()
	
	print("insert into users (name, lon, lat, color) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "')")
#	cur.execute("insert into users (name, lon, lat, color) values ('" + user["name"] + "', " + user["lon"] + ", " + user["lat"] + ", '" + user["color"] + "');")
	#cur.commit()
	#print(cur.statusmessage)
	return jsonify(user), 201

app.run(host = '192.168.1.3', port = 8000)

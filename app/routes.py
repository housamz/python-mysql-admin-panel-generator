from flask import render_template, flash, redirect, url_for, request
import pymysql
import json

from app import *
from app.form import ServerInfo
from app.handler import *


@app.route('/', methods=['GET', 'POST'])
def login():
	form = ServerInfo()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
			form.username.data, form.remember_me.data))
		return redirect(url_for('databases'))
	return render_template('index.html', form=form)


@app.route("/connect", methods=['GET', 'POST'])
def connect():
	try:
		mysql = pymysql.connect(
			request.form["host"],
			request.form["username"],
			request.form["password"],
			charset='utf8mb4'
		)
		data = connect_to_db(mysql, "SHOW DATABASES")
		result = ''
		for database in data:
			result += "<option value=\""+database[0]+"\">"+database[0]+"</option>"
		json_data = {"status": "success", "result": result}
		return json.dumps(json_data)
	except:
		json_data = {"status": "error", "message": "Couldn't connect to MySQL, check your credentials!"}
		return json_data


@app.route("/generate", methods=['GET', 'POST'])
def generate():
	mysql = pymysql.connect(
		request.form["host"],
		request.form["username"],
		request.form["password"],
		request.form["database"],
		charset='utf8mb4')
	data = generate_mage(mysql, request.form["createUsers"])
	return data

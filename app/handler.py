import os
from datetime import datetime
from shutil import copyfile
import random


# function to write directories
def write_dir(path):
	try:
		os.mkdir(path)
	except OSError:
		return "<li>Creation of the directory %s failed</li>" % path
	else:
		return "<li>Successfully created the directory %s</li>" % path


# function to write files
def write_file(filename, data):
	try:
		f = open(filename, "w+")
		f.write(data)
		f.close()
	except IOError:
		return "<li>Creation of the file %s failed</li>" % filename
	else:
		return "<li>Successfully created the file %s</li>" % filename


# function to copy files to locations
def copy_file(old_file, new_file):
	try:
		copyfile(old_file, new_file)
	except IOError:
		return "<li>Creation of the file %s failed</li>" % new_file
	else:
		return "<li>Successfully created the file %s</li>" % new_file


# connect to the database
def connect_to_db(mysql, query):
	cursor = mysql.cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	if data is None:
		return "Couldn't connect to MySQL database"
	else:
		return data


# generating a random icon for categories in the admin panel
def random_glyphicon():
	glyphicons = [
		"asterisk", "plus", "euro", "eur", "minus", "cloud", "envelope", "pencil", "glass", "music", "search",
		"heart", "star", "star-empty", "user", "film", "th-large", "th", "th-list", "ok", "remove", "zoom-in",
		"zoom-out", "off", "signal", "cog", "file", "time", "road", "download-alt", "download", "upload",
		"inbox", "play-circle", "repeat", "refresh", "list-alt", "lock", "flag", "headphones", "volume-off",
		"volume-down", "volume-up", "qrcode", "barcode", "tag", "tags", "book", "bookmark", "print", "camera",
		"font", "bold", "italic", "text-height", "text-width", "align-left", "align-center", "align-right",
		"align-justify", "list", "indent-left", "indent-right", "facetime-video", "picture", "map-marker",
		"adjust", "tint", "share", "check", "move", "step-backward", "fast-backward", "backward", "play",
		"pause", "stop", "forward", "fast-forward", "step-forward", "eject", "chevron-left", "chevron-right",
		"plus-sign", "minus-sign", "remove-sign", "ok-sign", "question-sign", "info-sign", "screenshot",
		"remove-circle", "ok-circle", "ban-circle", "arrow-left", "arrow-right", "arrow-up", "arrow-down",
		"share-alt", "resize-full", "resize-small", "exclamation-sign", "gift", "leaf", "fire", "eye-open",
		"eye-close", "warning-sign", "plane", "calendar", "random", "comment", "magnet", "chevron-up",
		"chevron-down", "retweet", "shopping-cart", "folder-close", "folder-open", "resize-vertical",
		"resize-horizontal", "hdd", "bullhorn", "bell", "certificate", "thumbs-up", "thumbs-down",
		"hand-right", "hand-left", "hand-up", "hand-down", "circle-arrow-right", "circle-arrow-left",
		"circle-arrow-up", "circle-arrow-down", "globe", "wrench", "tasks", "filter", "briefcase",
		"fullscreen", "dashboard", "paperclip", "heart-empty", "link", "phone", "pushpin", "usd", "gbp",
		"sort", "sort-by-alphabet", "sort-by-alphabet-alt", "sort-by-order", "sort-by-order-alt",
		"sort-by-attributes", "sort-by-attributes-alt", "unchecked", "expand", "collapse-down", "collapse-up",
		"log-in", "flash", "new-window", "record", "save", "open", "saved", "import", "export", "send",
		"floppy-disk", "floppy-saved", "floppy-remove", "floppy-save", "floppy-open", "credit-card",
		"transfer", "cutlery", "header", "compressed", "earphone", "phone-alt", "tower", "stats", "sd-video",
		"hd-video", "subtitles", "sound-stereo", "sound-dolby", "sound-5-1", "sound-6-1", "sound-7-1",
		"copyright-mark", "registration-mark", "cloud-download", "cloud-upload", "tree-conifer",
		"tree-deciduous", "cd", "save-file", "open-file", "level-up", "copy", "paste", "alert", "equalizer",
		"king", "queen", "pawn", "bishop", "knight", "baby-formula", "tent", "blackboard", "bed", "apple",
		"erase", "hourglass", "lamp", "duplicate", "piggy-bank", "scissors", "bitcoin", "btc", "xbt", "yen",
		"jpy", "ruble", "rub", "scale", "ice-lolly", "ice-lolly-tasted", "education", "option-horizontal",
		"option-vertical", "menu-hamburger", "modal-window", "oil", "grain", "sunglasses", "text-size",
		"text-color", "text-background", "object-align-top", "object-align-bottom", "object-align-horizontal",
		"object-align-left", "object-align-vertical", "object-align-right", "triangle-right", "triangle-left",
		"triangle-bottom", "triangle-top", "console", "superscript", "subscript", "menu-left", "menu-right",
		"menu-down", "menu-up"]
	return random.choice(glyphicons)


# generating the code
def generate_mage(mysql, create_users):
	# create cursor
	cursor = mysql.cursor()

	# generate the directory to hold the project
	path = "generated/" + getattr(mysql, 'db').decode('utf-8') + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

	# gather success info and display to user at the end
	message = "Your new MAGE panel is located in: <strong>" + path + "<br><br>"
	message += "The operations that were performed are: </strong><ul>"

	# write the project directories
	message += write_dir(path)
	message += write_dir(path + "/templates")
	message += write_dir(path + "/static")

	# load all tables in database
	cursor.execute("SHOW TABLES")
	get_all_tables = cursor.fetchall()
	tables = [a[0] for a in get_all_tables]

	# create the users table and add a dummy user
	if create_users == "true":
		if "users" not in tables:
			cursor.execute("""
				CREATE TABLE IF NOT EXISTS `users`
				(`id` int NOT NULL AUTO_INCREMENT, 
				`name` varchar(255) NOT NULL, 
				`email` varchar(255) NOT NULL, 
				`password` varchar(255) NOT NULL, 
				`role` int NOT NULL, PRIMARY KEY (`id`) ) 
				ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1
			""")

			# inserting the entry for admin, password is MD5'ed
			cursor.execute("""INSERT INTO users (name, email, password, role)
				VALUES (
				'Admin', 
				'admin@example.org', 
				'pbkdf2:sha256:150000$R5Mx0zoD$92ad711a1ee26a70f9483779154355c30c10aac29ec5e8c36173778f706131f6',
				1)""")
			mysql.commit()

			# add the 'users' table to the list of tables and sort the list
			tables.append('users')
			tables.sort()

	# the generation process starts here
	# adding the basic structure of app.py
	the_app = """from flask import Flask, render_template, request, redirect, session, url_for
from flaskext.mysql import MySQL
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from handler import *

app = Flask(__name__)
app.secret_key = 'Mage is the best!'

# MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = "{0}"
app.config['MYSQL_DATABASE_PASSWORD'] = "{1}"
app.config['MYSQL_DATABASE_DB'] = "{2}"
app.config['MYSQL_DATABASE_HOST'] = "{3}"
mysql.init_app(app)


def login_required(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		if 'authorised' not in session:
			return render_template('login.html')
		return f(*args, **kwargs)
	return wrapped


@app.context_processor
def inject_tables_and_counts():
	data = count_all(mysql)
	return dict(tables_and_counts=data)


@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html')

""".format(
		getattr(mysql, 'user').decode('utf-8'),
		getattr(mysql, 'password').decode('utf-8'),
		getattr(mysql, 'db').decode('utf-8'),
		getattr(mysql, 'host')
	)

	# adding the project sidebar
	sidebar = """
<!-- Sidebar Holder -->
<nav id="sidebar" class="bg-primary">
	<div class="sidebar-header">
		<h3>
			{0} Admin<br>
			<i id="sidebarCollapse" class="glyphicon glyphicon-circle-arrow-left"></i>
		</h3>
		<strong>
			{0}<br>
			<i id="sidebarExtend" class="glyphicon glyphicon-circle-arrow-right"></i>
		</strong>
		
	</div><!-- /sidebar-header -->
	<!-- start sidebar -->
	<ul class="list-unstyled components">
		<li>
			<a href="./" aria-expanded="false">
				<i class="glyphicon glyphicon-home"></i>
				Home
			</a>
		</li>""".format(
		getattr(mysql, 'db').decode('utf-8').title())

	# loop through the tables in the database
	for (index, table_name) in enumerate(tables):

		# loading all the columns in a table and getting the primary key
		cursor.execute("DESC " + table_name)
		all_columns = cursor.fetchall()
		modifier = all_columns[0]

		# adding a corresponding link in the sidebar for each table
		icon = random_glyphicon()
		sidebar += """
<li>
	<a href="/%s">
		<i class="glyphicon glyphicon-%s"></i>
		%s
		<span class="pull-right">{{tables_and_counts.%s.1}}</span>
	</a>
</li>\n""" % (
			table_name,
			icon,
			table_name.replace("_", " ").title(),
			index)

		# adding corresponding route for each table in the database
		the_app += """
@app.route("/{0}")
@login_required
def {0}():
	data = fetch_all(mysql, "{0}")
	return render_template('{0}.html', data=data, table_count=len(data))


@app.route('/edit_{0}/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_{0}(modifier_id, act):
	if act == "add":
		return render_template('edit_{0}.html', data="", act="add")
	else:
		data = fetch_one(mysql, "{0}", "{1}", modifier_id)
	
		if data:
			return render_template('edit_{0}.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id

""".format(
			table_name,
			modifier[0]
		)

		# adding the corresponding 'display' page for each table
		current_html_page = """
{% extends "base.html" %}

{% block content %}
	<a class="btn btn-primary" href="./edit_""" + table_name + """/add/0">
		<i class="glyphicon glyphicon-plus-sign"></i> Add New %s
	</a>
	<h1>%s</h1>
	<p>This table includes {{table_count}} %s</p>
	<table id="sorted" class="table table-striped table-bordered">
		<thead>""" % (
			table_name.title(),
			table_name.replace("_", " ").title(),
			table_name
		)

		# adding the corresponding 'create/update' page for each table
		current_html_edit_page = """
{% extends "base.html" %}

{% block content %}
	<form method="post" action="{{ url_for('save') }}" enctype='multipart/form-data'>
		<fieldset>
			<legend class="hidden-first">Add New """ + table_name.title() + """</legend>
			<input name="cat" type="hidden" value='""" + table_name + """'>
			<input name="modifier" type="hidden" value='""" + modifier[0] + """'>
			<input name="id" type="hidden" value="{{data[0]}}">
			<input name="act" type="hidden" value="{{act}}">
		"""

		current_html_page_head = ''

		# loop through the columns of each tables
		# and then adding an update field for each
		for (i, column) in enumerate(all_columns):
			current_html_page_head += "\t\t\t\t<th>" + column[0].replace("_", " ").title() + "</th>\n"

			if column[3] != "PRI":
				if column[1] == "text":
					current_html_edit_page += """
			<label>""" + column[0].replace("_", " ").title() + """</label>
			<textarea 
				class ="ckeditor 
				form-control" 
				name=\"""" + column[0] + """\">{{data[""" + str(i) + """]}}</textarea><br>"""
				else:
					current_html_edit_page += """
			<label>""" + column[0].replace("_", " ").title() + """</label>
			<input 
				class="form-control" 
				type="text" 
				name=\"""" + column[0] + """\"
				value="{{data[""" + str(i) + """]}}" /><br>"""

		current_html_page += """\n\t\t\t<tr>\n""" + current_html_page_head + """
				<th>Edit</th>
				<th>Delete</th>
			</tr>
		</thead>\n"""

		current_html_edit_page += """<br>
			<input type="submit" value=" Save " class="btn btn-success">
		</fieldset>
	</form>
{% endblock %}"""

		current_html_page += """\t\t<tbody>
			{% for row_data in data %}
			<tr>
				{% for d in row_data %}
					<td>{{d}}</td>
				{% endfor %}
				<td>
					<a href="./edit_""" + table_name + """/edit/{{row_data[0]}}">
						<i class="glyphicon glyphicon-edit"></i>
					</a>
				</td>
				<td>
					<a 
						href="./save?cat=""" + table_name + """&act=delete&modifier=""" + modifier[0] + """&id={{row_data[0]}}"
						onclick="return navConfirm(this.href);">
					<i class="glyphicon glyphicon-trash"></i>
					</a>
					</td>
			</tr>
			{% endfor %}
		</tbody>
	</table>
{% endblock %}"""

		# writing files for 'create/update/display' for each table
		current_page_template = path + "/templates/%s.html" % table_name
		current_edit_page_template = path + "/templates/edit_%s.html" % table_name

		message += write_file(current_page_template, current_html_page)
		message += write_file(current_edit_page_template, current_html_edit_page)

	sidebar += """
		<li><a href="/logout"><i class="glyphicon glyphicon-log-out"></i> Logout</a></li>
	</ul>
	<div class ="visit">
		<p class ="text-center">Created using Python MAGE &hearts;</p>
		<a href ="https://github.com/housamz/python-mysql-admin-panel-generator" target="_blank" >Visit Project</a>
	</div>
</nav><!-- / end sidebar -->"""

	# finishing general routes in the app.py file
	the_app += """
@app.route('/save', methods=['GET', 'POST'])
@login_required
def save():
	cat = ''
	if request.method == 'POST':
		post_data = request.form.to_dict()
		if 'password' in post_data:
			post_data['password'] = generate_password_hash(post_data['password']) 
		if post_data['act'] == 'add':
			cat = post_data['cat']
			insert_one(mysql, cat, post_data)
		elif post_data['act'] == 'edit':
			cat = post_data['cat']
			update_one(mysql, cat, post_data, post_data['modifier'], post_data['id'])
	else:
		if request.args['act'] == 'delete':
			cat = request.args['cat']
			delete_one(mysql, cat, request.args['modifier'], request.args['id'])
	return redirect("./" + cat)


@app.route('/login')
def login():
	if 'authorised' in session:
		return redirect(url_for('index'))
	else:
		error = request.args['error'] if 'error' in request.args else ''
		return render_template('login.html', error=error)


@app.route('/login_handler', methods=['POST'])
def login_handler():
	try:
		email = request.form['email']
		password = request.form['password']
		data = fetch_one(mysql, "users", "email", email)
		
		if data and len(data) > 0:
			if check_password_hash(data[3], password):
				session['authorised'] = 'authorised',
				session['id'] = data[0]
				session['name'] = data[1]
				session['email'] = data[2]
				session['role'] = data[4]
				return redirect(url_for('index'))
			else:
				return redirect(url_for('login', error='Wrong Email address or Password.'))
		else:
			return redirect(url_for('login', error='No user'))
	
	except Exception as e:
		return render_template('login.html', error=str(e))


@app.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(debug=True)
"""
	# copying files from MAGE library to the project
	message += copy_file("library/base.html", path + "/templates/base.html")
	message += copy_file("library/index.html", path + "/templates/index.html")
	message += copy_file("library/login.html", path + "/templates/login.html")
	message += copy_file("library/style.css", path + "/static/style.css")
	message += copy_file("library/handler.py", path + "/handler.py")
	message += copy_file("library/requirements.txt", path + "/requirements.txt")

	# writing final files
	message += write_file(path + "/templates/sidebar.html", sidebar)
	message += write_file(path + "/app.py", the_app)
	message += "</ul><br>"

	message += '<a class="btn btn-info center-block" href="./">Create Again!</a>'

	json_data = {"status": "finished", "message": message}

	return json_data

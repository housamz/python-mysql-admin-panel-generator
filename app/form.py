from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import InputRequired


class ServerInfo(FlaskForm):
	host = StringField('Host', validators=[InputRequired()])
	username = StringField('Username', validators=[InputRequired()])
	password = PasswordField('Password')
	create_users = BooleanField('Create Users table in the database', validators=[InputRequired()])
	connect_button = SubmitField('Understood, Next Step >')
	databases = SelectField('Select your database', choices=[(' ', 'Please Select')])
	generate_button = SubmitField('Generate Admin Panel')

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators, DateField
from wtforms.validators import Required


class LoginForm(Form):
	username = TextField('username', validators = [Required()])
	password = TextField('password', validators = [Required()])
	

class AddContactForm(Form):
	name = TextField('name', validators = [Required()])
	number = TextField('number', validators = [Required()])
	description = TextField('description', validators = [Required()])

	
class AddUserForm(Form):
	username = TextField('username', validators = [Required()])
	password = TextField('password', validators = [Required()])
	
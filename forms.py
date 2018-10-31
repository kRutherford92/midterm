# Import libraries
# From wtforms import Fields
# Import Validators
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# Create class LoginForm
class LoginForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired()])
	password=PasswordField('Password', validators=[DataRequired()])
	submit=SubmitField('Login')

# Create class SignupForm
class SignupForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired()])
	password=PasswordField('Password', validators=[DataRequired()])
	repeatPassword=PasswordField('Repeat Password', validators=[DataRequired()])
	submit=SubmitField('Signup')


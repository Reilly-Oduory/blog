from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, EqualTo, ValidationError, Required, Length
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address', validators = [Required('Email is Required'),Email()])
    username = StringField('Enter your username',validators = [Required('username is required')])
    password = PasswordField('Password',validators = [Required('Password is required'), EqualTo('password_confirm',message = 'Passwords must match'), Length(min=8, max=16,message='Your password must be between 8 to 16 characters long')])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required('You must confirm your password')])

    def validate_email(self, data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required('You have to enter email'),Email()])
    password = PasswordField('Password',validators =[Required('You have to enter your password')])
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import Required


class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[Required()])
    content = TextAreaField('Post Content', validators=[Required()])


class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[Required()])

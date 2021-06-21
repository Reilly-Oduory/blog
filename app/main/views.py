from flask import render_template, url_for
from . import main

@main.route("/")
def index():
    title = 'Welcome'

    return render_template('index.html', title = title)
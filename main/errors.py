from . import main
from flask import render_template


@main.app_errorhandler(404)
def page_not_found(e):
    # print(e)
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    return '<h1>server error</h1>', 500

import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint
from project.api.views import api_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_blueprint)


@app.errorhandler(404)
def not_found(error):
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log','a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write(f'\n404 error: at {current_timestamp}: {r}\n')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log','a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write(f'\n 404 error at : {current_timestamp}:  {r}\n')
    return render_template('500.html'),500
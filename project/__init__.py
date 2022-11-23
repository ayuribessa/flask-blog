import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api

app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# api = Api(app)

from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint
# from project.api.views import api_blueprint
from project.api import api_bp

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_bp, url_prefix='/api/v1/')
# https://stackoverflow.com/questions/38448618/using-flask-restful-as-a-blueprint-in-large-application
# https://flask-restful.readthedocs.io/en/latest/intermediate-usage.html
# https://dev.to/paurakhsharma/flask-rest-api-part-2-better-structure-with-blueprint-and-flask-restful-2n93
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
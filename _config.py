import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLET = True
SECRET_KEY = '@?"v<kn8p6k?uml'

DATABASE_PATH = os.path.join(basedir,DATABASE)
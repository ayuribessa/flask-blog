from functools import wraps
from flask import render_template, redirect, Blueprint, request, session, flash, url_for
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm
from project import db
from project.models import User

###### Configs #######
users_blueprint = Blueprint('users',__name__)

##### Helper Functions ######
def login_required(test):
   @wraps(test)
   def wrap(*args, **kwargs):
      if 'logged_in' in session:
         return test(*args, **kwargs)
      else:
         flash('You need to login first.')
         return redirect(url_for('users.login'))
   return wrap

##### Routes ######
@users_blueprint.route('/logout/')
@login_required
def logout():
   session.pop('logged_in',None)
   session.pop('user_id',None)
   session.pop('role',None)
   flash('Goodbye !')
   return redirect(url_for('users.login'))


@users_blueprint.route('/login/',methods = ['GET', 'POST'])
def login():
   error = None
   form = LoginForm(request.form)
   if request.method == 'POST':
      if form.validate():
         user = User.query.filter_by(name=request.form['name']).first()
         if User is not None and user.password == request.form['password']:
            session['logged_in'] = True 
            session['user_id'] = user.id 
            session['role'] = user.role 
            flash('Welcome')
            return redirect(url_for('tasks.tasks'))
         else:
            error = 'Invalid username or password'
   else:
      return render_template('login.html',form=form, error= error)
      
      
   
   

     



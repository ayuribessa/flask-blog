from functools import wraps
from flask import render_template, redirect, Blueprint, request, session, flash, url_for
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm
from project import db, bcrypt
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
   session.pop('name',None)
   flash('Goodbye !')
   return redirect(url_for('users.login'))


@users_blueprint.route('/',methods = ['GET', 'POST'])
def login():
   error = None
   form = LoginForm(request.form)
   if request.method == 'POST':
      if form.validate():
         user = User.query.filter_by(name=request.form['name']).first()
         if User is not None and bcrypt.check_password_hash(user.password, request.form['password']):
            session['logged_in'] = True 
            session['user_id'] = user.id 
            session['role'] = user.role 
            session['user'] = user.name
            flash('Welcome')
            return redirect(url_for('tasks.tasks'))
         else:
            error = 'Invalid username or password'
   else:
      return render_template('login.html',form=form, error= error)
      
@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
   error = None
   form = RegisterForm(request.form)
   if request.method == 'POST':
      new_user = User(
         form.data["name"],
         form.data["email"],
         bcrypt.generate_password_hash(form.data["password"]),
      )
      try:
         db.session.add(new_user)
         db.session.commit()
         flash('Thanks for Registering. Please Login.')
         return redirect(url_for('users.login'))
      except IntegrityError:
         error = 'That username and/or password already exist.'
         return render_template('register.html', form=form,error=error)
   else:
      return render_template('register.html',form=form, error=error)
   
   

     



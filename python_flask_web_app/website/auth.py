from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

#decorator accepts route 
@auth.route('/login', methods = ['GET','POST'])
def login():
    data = request.form
    print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #query for user who logged in
        user = User.query.filter_by(email = email).first()
        
        #verify pass with database pass
        if user:
            if check_password_hash(user.password, password):
                flash('wow u did it nice', category = 'success')
                login_user(user, remember = True)
                #can redirect to '/' but if changed the syntax for '/' will be invalid so use the following:
                return redirect(url_for('views.home'))
            else:
                flash('incorrect pass dickhead, try again ', category = 'error')
        else:
            flash('nuh-uh u havent signed up hoe', category = 'error')

    return render_template("login.html", text = "- yizhe", boolean = True, user = current_user)


@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
@auth.route('/sign_up', methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #query for user who logged in
        user = User.query.filter_by(email = email).first()

        if user:
            flash('email already exist dinggus', category = 'error')
        elif len(email) < 4:
            flash('Email shorter than 4 char', category = 'error')
        elif len(firstname) < 2:
            flash('firstname shorter than 2 char', category = 'error')
        elif password1 != password2:
            flash('pass error', category = 'error')
        elif len(password1) < 7:
            flash('len pass less than 7 char', category = 'error')
        else:
            new_user = User(email = email, firstname = firstname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash('acc created', category = 'success')
            #can redirect to '/' but if changed the syntax for '/' will be invalid so use the following:
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user = current_user)
from flask_login import login_user, login_required, logout_user

from app import app, db
from flask import render_template, request, redirect, flash, url_for
from models import User, Task
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()
    return render_template('index.html', data=users)


@app.route('/tasks')
def tasks():
    return render_template('tasks.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not(login or password or password2):
            flash('Пожалуйста заполните все поля!')
        elif password != password2:
            flash('Пароли не совпадают!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('auth.html')


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('profile'))
        else:
            flash('Логин или пароль некорректны')
    else:
        flash('Пожалуйста, заполните поля "Логин" и "Пароль"')

    return render_template('login_page.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_post', methods=['POST'])
@login_required
def add_post():
    if request.method == "POST":
        task_name = request.form['task_name']
        task = request.form['task']

        task = Task(task_name=task_name, task=task)

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/add_post')
        except:
            return "Получилась ошибка"
    else:
        return render_template('add_post.html')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response

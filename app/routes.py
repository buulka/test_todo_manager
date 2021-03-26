from flask_login import login_user, login_required, logout_user, current_user

from app import app, db
from flask import render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, Task


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
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
            return show_posts()
        else:
            flash('Логин или пароль некорректны')
    else:
        flash('Пожалуйста, заполните поля "Логин" и "Пароль"')

    return render_template('login_page.html')


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    task_name = request.form.get('task_name')
    task = request.form.get('task')

    if request.method == "POST":

        task = Task(task_name=task_name, task=task, user_id=current_user.id)

        db.session.add(task)
        db.session.commit()

        return redirect('/profile')

    else:
        return render_template('add_post.html')


@app.route('/posts', methods=['GET', 'POST'])
@login_required
def show_posts():
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()

    return render_template('posts.html', data=user_tasks)


@app.route('/delete_post/<post_id>')
def delete_post(post_id):
    Task.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(url_for('show_posts'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response

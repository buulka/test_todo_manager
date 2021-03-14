from app import app
from flask import render_template, request, redirect
from models import User, Task, db


@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()
    return render_template('index.html', data=users)


@app.route('/tasks')
def tasks():
    return render_template('tasks.html')


@app.route('/auth')
def auth():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']

        user = User(login=login, password=password)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/auth')
        except:
            return "Получилась ошибка"
    else:
        return render_template('auth.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        pass
    else:
        render_template('auth.html')


@app.route('logout', methods=['GET', 'POST'])
def logout():
    pass


@app.route('/add_post', methods=['POST'])
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

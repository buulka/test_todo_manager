from app import app
from flask import render_template, request, redirect
# from authorize_db import User, db



@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()
    return render_template('index.html', data=users)


@app.route('/tasks')
def tasks():
    return render_template('tasks.html')


# @app.route('/auth', methods=['POST', 'GET'])
# def auth():
#     if request.method == "POST":
#         login = request.form['login']
#         password = request.form['password']
#
#         user = User(login=login, password=password)
#
#         try:
#             db.session.add(user)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return "Получилась ошибка"
#     else:
#         return render_template('auth.html')


@app.route('/add_post')
def add_post():
    return render_template('add_post.html')

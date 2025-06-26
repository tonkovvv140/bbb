import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager(app)
login_manager.login_view = 'login'

def init_db():
    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE,
            password_hash TEXT)""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                author TEXT,
                date TEXT,
                article_text TEXT
            )
            """)
        db.commit()


class User(UserMixin):
    def __init__(self, id):
        self.id = str(id)

@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE id=?", (user_id,))
        user_row = cursor.fetchone()

    if user_row:
        return User(user_row[0])
    else:
        return None


@app.route("/article", methods=['GET', 'POST'])
@login_required
def articles():
    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()
        if request.method == 'POST':
            form_data = request.form
            author = form_data['author']
            name = form_data['name']
            date = form_data['date']
            article = form_data['article']

            cursor.execute(
                    'INSERT INTO articles (author, name, date, article_text) VALUES (?, ?, ?, ?)',
                    (author, name, date, article)
                )
            db.commit()


    return render_template("index.html")


@app.route("/articles/<int:id>")
def art(id):
    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()
        cursor.execute("SELECT author, name, date, article_text FROM articles WHERE id = ?", (id,))
        result = cursor.fetchone()

    if result is None:
        return "Статья не найдена"

    author, name, date, article = result
    return render_template("id.html", author=author, name=name, date=date, article=article)

@app.route("/article/all")
def all():
    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM articles")
        result = cursor.fetchall()

    print(result)
    return render_template("articles.html", result = result)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        with sqlite3.connect("DATABASE_PATH") as db:
            cursor = db.cursor()
            form_data = request.form
            login = form_data["login"]
            password = form_data["password"]
            repeat_password = form_data["repeat-password"]

            if password != repeat_password:

                return "Пароли не совпадают!"

            password_hash = generate_password_hash(password)
            cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
            existing_user = cursor.fetchone()


            if existing_user:

                return "Пользователь с таким логином уже существует!"
            else:
                cursor.execute("INSERT INTO users (login, password_hash) VALUES (?, ?)", (login, password_hash))
                db.commit()

            return redirect(url_for('login'))

    return render_template("register.html")


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        with sqlite3.connect("DATABASE_PATH ") as db:
            cursor = db.cursor()
            form_data = request.form
            login = form_data["login"]
            password = form_data["password"]

            cursor.execute("SELECT id, password_hash FROM users WHERE login = ?", [login])
            result = cursor.fetchone()

            if result is None:
                return "Неверный логин или пароль!"

            user_id, password_hash = result

            if check_password_hash(password_hash, password):
                user = User(user_id)
                login_user(user)
                return redirect(url_for('articles'))
            else:
                return "Неверный логин или пароль!"

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

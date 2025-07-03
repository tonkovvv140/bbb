import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
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

            return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth_bp.route("/login", methods = ['GET', 'POST'])
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
                return redirect(url_for('article.articles'))
            else:
                return "Неверный логин или пароль!"

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

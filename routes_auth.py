import sqlite3
import logging
import re
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(asctime)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)

def is_valid_login(login):
    return re.match(r'^[A-Za-z0-9_]{3,20}$', login)

def is_valid_password(password):
    return len(password) >= 6

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        logger.info("Обработка формы регистрации")
        with sqlite3.connect("DATABASE_PATH") as db:
            cursor = db.cursor()
            form_data = request.form
            login = form_data["login"]
            password = form_data["password"]
            repeat_password = form_data["repeat-password"]

            logger.info(f"Попытка регистрации: логин = {login}")

            if password != repeat_password:
                logger.warning("Пароли не совпадают")
                return "Пароли не совпадают!"

            password_hash = generate_password_hash(password)
            logger.info(f"Хеш пароля создан для пользователя: {login}")

            cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
            existing_user = cursor.fetchone()

            if existing_user:
                logger.warning(f"Регистрация отклонена: логин {login} уже занят")
                return "Пользователь с таким логином уже существует!"
            else:
                cursor.execute(
                    "INSERT INTO users (login, password_hash) VALUES (?, ?)",
                    (login, password_hash)
                )
                db.commit()
                logger.info(f"Пользователь успешно зарегистрирован: {login}")

        return redirect(url_for('auth.login'))

    logger.info("Открыта страница регистрации (GET-запрос)")
    return render_template("register.html")

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        logger.info("Обработка формы входа")
        with sqlite3.connect("DATABASE_PATH") as db:
            cursor = db.cursor()
            form_data = request.form
            login = form_data["login"]
            password = form_data["password"]

            logger.info(f"Попытка входа: логин = {login}")

            cursor.execute("SELECT id, password_hash FROM users WHERE login = ?", [login])
            result = cursor.fetchone()

            if result is None:
                logger.warning(f"Вход отклонён: пользователь {login} не найден")
                return "Неверный логин или пароль!"

            user_id, password_hash = result

            if check_password_hash(password_hash, password):
                user = User(user_id)
                login_user(user)
                logger.info(f"Вход выполнен успешно: {login}")
                return redirect(url_for('article.articles'))
            else:
                logger.warning(f"Вход отклонён: неправильный пароль для {login}")
                return "Неверный логин или пароль!"

    logger.info("Открыта страница входа (GET-запрос)")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    logger.info("Пользователь вышел из системы")
    return redirect(url_for('auth.login'))

import sqlite3
import logging
from flask import Blueprint, render_template, request
from flask_login import login_required

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(asctime)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

article_bp = Blueprint("article", __name__)

@article_bp.route("/article", methods=['GET', 'POST'])
@login_required
def articles():
    logger.info("Открыта страница добавления статьи")

    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()

        if request.method == 'POST':
            form_data = request.form
            author = form_data['author']
            name = form_data['name']
            date = form_data['date']
            article = form_data['article']

            logger.info(f"Добавление статьи: '{name}' от автора {author}")

            cursor.execute(
                'INSERT INTO articles (author, name, date, article_text) VALUES (?, ?, ?, ?)',
                (author, name, date, article)
            )
            db.commit()
            logger.info("Статья успешно добавлена в базу данных")

    return render_template("index.html")

@article_bp.route("/articles/<int:id>")
def art(id):
    logger.info(f"Запрошена статья с ID: {id}")

    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()
        cursor.execute("SELECT author, name, date, article_text FROM articles WHERE id = ?", (id,))
        result = cursor.fetchone()

    if result is None:
        logger.warning(f"Статья с ID {id} не найдена")
        return "Статья не найдена"

    author, name, date, article = result
    logger.info(f"Просмотр статьи: '{name}' от {author}")
    return render_template("id.html", author=author, name=name, date=date, article=article)

@article_bp.route("/article/all")
def all():
    logger.info("Запрошен список всех статей")

    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM articles")
        result = cursor.fetchall()

    logger.info(f"Найдено {len(result)} статей")
    return render_template("articles.html", result=result)

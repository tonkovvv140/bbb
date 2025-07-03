import sqlite3
from flask import Blueprint, render_template, request
from flask_login import login_required

article_bp = Blueprint("article", __name__)

@article_bp.route("/article", methods=['GET', 'POST'])
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


@article_bp.route("/articles/<int:id>")
def art(id):
    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()
        cursor.execute("SELECT author, name, date, article_text FROM articles WHERE id = ?", (id,))
        result = cursor.fetchone()

    if result is None:
        return "Статья не найдена"

    author, name, date, article = result
    return render_template("id.html", author=author, name=name, date=date, article=article)


@article_bp.route("/article/all")
def all():
    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM articles")
        result = cursor.fetchall()

    print(result)
    return render_template("articles.html", result = result)

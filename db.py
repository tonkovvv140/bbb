import sqlite3

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

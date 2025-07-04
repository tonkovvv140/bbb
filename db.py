import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(asctime)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

def init_db():
    logger.info("Подключение к базе данных")

    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()

        logger.info("Создание таблицы пользователей")
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE,
            password_hash TEXT)""")

        logger.info("Создание таблицы статей")
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
        logger.info("База данных успешно инициализирована.")

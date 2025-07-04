import sqlite3
import logging
from flask_login import UserMixin

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(asctime)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

class User(UserMixin):
    def __init__(self, id):
        self.id = str(id)

def load_user(user_id):
    logger.info(f"Загрузка пользователя с ID: {user_id}")

    with sqlite3.connect("DATABASE_PATH") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE id=?", (user_id,))
        user_row = cursor.fetchone()

    if user_row:
        logger.info(f"Пользователь с ID {user_id} найден")
        return User(user_row[0])
    else:
        logger.warning(f"Пользователь с ID {user_id} не найден")
        return None

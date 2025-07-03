import os
from flask import Flask
from flask_login import LoginManager
from db import init_db
from models import load_user
from routes_auth import auth_bp
from routes import article_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.user_loader(load_user)

app.register_blueprint(auth_bp)
app.register_blueprint(article_bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

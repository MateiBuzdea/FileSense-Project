from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Will use default flask authentication
login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect(app)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Register blueprints
from app.accounts.views import accounts_bp
from app.core.views import core_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)


# Default view
@app.route("/")
def index():
    return render_template("index.html")

# Static files
@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory(app.config["STATIC_FOLDER"], path)
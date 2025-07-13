from flask import Flask # type: ignore
from dotenv import load_dotenv # type: ignore
import app.database as db

def create_app():
    load_dotenv()
    db.init_db()
    app = Flask(__name__)

    from .routes import routes_user
    app.register_blueprint(routes_user.user_bp)

    from .routes import routes_point
    app.register_blueprint(routes_point.point_bp)

    return app
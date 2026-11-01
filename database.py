import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from config import Config, BASE_DIR

logger = logging.getLogger(__name__)

db = SQLAlchemy()

def init_db(app):
    """
    Initializes SQLAlchemy with the Flask app.
    Tests the database connection. If MySQL fails, gracefully falls back to SQLite.
    """
    configured_uri = Config.get_database_uri()
    
    # Test connection if MySQL is configured
    if configured_uri.startswith("mysql"):
        try:
            logger.info("Attempting connection to MySQL database...")
            test_engine = create_engine(configured_uri, connect_args={"connect_timeout": 3})
            with test_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Successfully connected to MySQL database.")
            app.config["SQLALCHEMY_DATABASE_URI"] = configured_uri
            app.config["DB_ENGINE_TYPE"] = "MySQL (Production)"
        except Exception as e:
            fallback_path = BASE_DIR / "quoteflow.db"
            fallback_uri = f"sqlite:///{fallback_path}"
            logger.warning(
                f"MySQL connection failed ({e}). Gracefully falling back to local SQLite: {fallback_uri}"
            )
            app.config["SQLALCHEMY_DATABASE_URI"] = fallback_uri
            app.config["DB_ENGINE_TYPE"] = "SQLite (Local Fallback - configure MySQL in .env)"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = configured_uri
        app.config["DB_ENGINE_TYPE"] = "SQLite (Local Storage)"
        
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    with app.app_context():
        # Import models to ensure they are registered before create_all
        import models
        db.create_all()
        logger.info(f"Database initialized successfully with {app.config['DB_ENGINE_TYPE']}.")

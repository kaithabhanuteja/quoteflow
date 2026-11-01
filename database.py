# import logging
# import os
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine, text
# from config import Config, BASE_DIR

# logger = logging.getLogger(__name__)

# db = SQLAlchemy()

# def init_db(app):
#     """
#     Initializes SQLAlchemy with the Flask app.
#     Tests the database connection. If MySQL fails, gracefully falls back to SQLite.
#     """
#     configured_uri = Config.get_database_uri()
    
#     # Test connection if MySQL is configured
#     if configured_uri.startswith("mysql"):
#         try:
#             logger.info("Attempting connection to MySQL database...")
#             test_engine = create_engine(configured_uri, connect_args={"connect_timeout": 3})
#             with test_engine.connect() as conn:
#                 conn.execute(text("SELECT 1"))
#             logger.info("Successfully connected to MySQL database.")
#             app.config["SQLALCHEMY_DATABASE_URI"] = configured_uri
#             app.config["DB_ENGINE_TYPE"] = "MySQL (Production)"
#         except Exception as e:
#             if os.getenv("VERCEL") == "1":
#                 raise RuntimeError(
#                     f"MySQL connection failed on Vercel: {e}"
#                 ) from e

#             fallback_path = BASE_DIR / "quoteflow.db"
#             fallback_uri = f"sqlite:///{fallback_path}"

#             logger.warning(
#                  f"MySQL unavailable. Using local SQLite: {e}"
#             )

#             app.config["SQLALCHEMY_DATABASE_URI"] = fallback_uri
#             app.config["DB_ENGINE_TYPE"] = "SQLite (Local Fallback)"
#     else:
#         app.config["SQLALCHEMY_DATABASE_URI"] = configured_uri
#         app.config["DB_ENGINE_TYPE"] = "SQLite (Local Storage)"
        
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.init_app(app)
    
#     with app.app_context():
#         # Import models to ensure they are registered before create_all
#         import models
#         db.create_all()
#         logger.info(f"Database initialized successfully with {app.config['DB_ENGINE_TYPE']}.")


import logging
import os
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy
from config import Config, BASE_DIR

logger = logging.getLogger(__name__)

db = SQLAlchemy()


def init_db(app):
    """
    Initializes SQLAlchemy.

    Vercel:
        Uses temporary SQLite for demonstration.
        Does not attempt a MySQL connection.

    Local:
        Uses the existing MySQL configuration.
        Falls back to local SQLite if MySQL is unavailable.
    """

    is_vercel = os.getenv("VERCEL") == "1"

    # ------------------------------------------------
    # VERCEL DEMO CONFIGURATION
    # ------------------------------------------------
    if is_vercel:

        database_path = Path("/tmp/quoteflow.db")
        database_path.parent.mkdir(parents=True, exist_ok=True)

        database_uri = f"sqlite:///{database_path}"

        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
        app.config["DB_ENGINE_TYPE"] = "SQLite (Vercel Demo)"

        logger.info("Using temporary SQLite database on Vercel.")

    # ------------------------------------------------
    # LOCAL DEVELOPMENT CONFIGURATION
    # ------------------------------------------------
    else:

        configured_uri = Config.get_database_uri()

        if configured_uri.startswith("mysql"):

            try:
                logger.info("Attempting connection to local MySQL...")

                from sqlalchemy import create_engine, text

                test_engine = create_engine(
                    configured_uri,
                    connect_args={"connect_timeout": 3}
                )

                with test_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))

                test_engine.dispose()

                app.config["SQLALCHEMY_DATABASE_URI"] = configured_uri
                app.config["DB_ENGINE_TYPE"] = "MySQL (Local)"

                logger.info("Successfully connected to MySQL.")

            except Exception as e:

                fallback_path = BASE_DIR / "quoteflow.db"
                fallback_uri = f"sqlite:///{fallback_path}"

                logger.warning(
                    "Local MySQL unavailable. Using SQLite fallback: %s",
                    e
                )

                app.config["SQLALCHEMY_DATABASE_URI"] = fallback_uri
                app.config["DB_ENGINE_TYPE"] = "SQLite (Local Fallback)"

        else:

            app.config["SQLALCHEMY_DATABASE_URI"] = configured_uri
            app.config["DB_ENGINE_TYPE"] = "SQLite (Local Storage)"

    # ------------------------------------------------
    # SQLALCHEMY INITIALIZATION
    # ------------------------------------------------

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"check_same_thread": False}
        }

    db.init_app(app)

    # ------------------------------------------------
    # DATABASE TABLE INITIALIZATION
    # ------------------------------------------------

    with app.app_context():

        # Import models before creating tables
        import models

        db.create_all()

        logger.info(
            "Database initialized successfully: %s",
            app.config["DB_ENGINE_TYPE"]
        )

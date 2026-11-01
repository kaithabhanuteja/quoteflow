import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.getenv("SECRET_KEY", "quoteflow-enterprise-secret-key-2026")
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Database Configuration
    # Defaults to MySQL if credentials provided; otherwise gracefully falls back to SQLite
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "quoteflow_db")
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # PDF and Upload Storage
    STORAGE_DIR = BASE_DIR / "static" / "generated_pdfs"
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Company Profile for Quotations
    COMPANY_NAME = os.getenv("COMPANY_NAME", "Quotflow Technologies Limited")
    COMPANY_TAGLINE = "Enterprise Cloud & AI Solutions"
    COMPANY_ADDRESS = "Madhapur, HITEC City, Hyderabad, Telangana, India"
    COMPANY_EMAIL = "contact@quotflow.ai"
    COMPANY_PHONE = "+91 (40) 6789-FLOW"
    COMPANY_WEBSITE = "https://www.quotflow.ai"
    COMPANY_TAX_ID = "GSTIN: 36AAACQ1234F1Z5"
    DEVELOPER_NAME = "Kaitha Bhanuteja"
    
    # Default Financial Parameters
    DEFAULT_CURRENCY = "INR"
    DEFAULT_TAX_RATE = 0.18        # 18% GST / Standard Tax
    DEFAULT_CONTINGENCY = 0.10     # 10% Risk Buffer
    DEFAULT_VALIDITY_DAYS = 30     # Quotation valid for 30 days

    @classmethod
    def get_database_uri(cls):
        """
        Determines the appropriate database URI.
        Attempts to connect to MySQL if configured, else seamlessly falls back to SQLite.
        """
        if cls.DATABASE_URL:
            return cls.DATABASE_URL
            
        if cls.MYSQL_PASSWORD or os.getenv("USE_MYSQL", "false").lower() == "true":
            # Attempt MySQL connection string with pymysql
            return f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}"
        
        # SQLite fallback for zero-friction local run
        db_path = BASE_DIR / "quoteflow.db"
        return f"sqlite:///{db_path}"

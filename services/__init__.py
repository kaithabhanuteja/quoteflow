from services.industry_config import get_industry_profile, INDUSTRY_PROFILES
from services.sample_emails import SAMPLE_EMAILS
from services.gemini_analyzer import analyze_email_with_gemini
from services.estimator import calculate_project_estimates, BASE_RATE_CARD, format_inr
from services.pdf_generator import generate_quotation_pdf

__all__ = [
    "get_industry_profile",
    "INDUSTRY_PROFILES",
    "SAMPLE_EMAILS",
    "analyze_email_with_gemini",
    "calculate_project_estimates",
    "BASE_RATE_CARD",
    "format_inr",
    "generate_quotation_pdf",
]

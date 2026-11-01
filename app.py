import os
import json
import logging
import random
from datetime import datetime, timezone
from flask import (
    Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
)
from flask_cors import CORS

from config import Config
from database import db, init_db
from models import Customer, Project, Quotation, QuotationVersion, ActivityLog
from services import (
    SAMPLE_EMAILS,
    get_industry_profile,
    analyze_email_with_gemini,
    calculate_project_estimates,
    generate_quotation_pdf,
    BASE_RATE_CARD,
    format_inr
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("quoteflow")

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize Database (MySQL with SQLite local fallback)
init_db(app)

# Register Template Filter and Global Context Variables
@app.template_filter("inr")
def jinja_inr_filter(amount, decimals=2):
    return format_inr(amount, include_symbol=True, decimals=decimals)

@app.context_processor
def inject_global_template_vars():
    return {
        "developer_name": Config.DEVELOPER_NAME,
        "company_name": Config.COMPANY_NAME,
        "company_tagline": Config.COMPANY_TAGLINE,
        "company_location": Config.COMPANY_ADDRESS,
        "company_email": Config.COMPANY_EMAIL,
        "company_phone": Config.COMPANY_PHONE,
        "company_website": Config.COMPANY_WEBSITE,
        "company_tax_id": Config.COMPANY_TAX_ID,
        "currency_symbol": "₹",
        "currency_code": "INR",
        "format_inr": format_inr
    }


# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------

def generate_reference_number(industry_name: str) -> str:
    """
    Generates a unique, standardized Quotation Reference Number.
    e.g. QF-2026-MED-4821 or QF-2026-FIN-9204
    """
    profile = get_industry_profile(industry_name)
    code = profile.get("code", "PRJ")
    year = datetime.now().year
    rand_num = random.randint(1000, 9999)
    return f"QF-{year}-{code}-{rand_num}"


# -------------------------------------------------------------
# WEB PAGES
# -------------------------------------------------------------

@app.route("/")
def landing():
    """Landing page - Professional SaaS homepage."""
    return render_template("landing.html")


@app.route("/studio")
def index():
    """Main Quotation Creation & AI Automation Studio."""
    return render_template(
        "index.html",
        sample_emails=SAMPLE_EMAILS,
        company_name=Config.COMPANY_NAME,
        db_type=app.config.get("DB_ENGINE_TYPE", "SQLite"),
        has_gemini_key=bool(Config.GEMINI_API_KEY)
    )


@app.route("/quotations")
def quotations_dashboard():
    """Quotation Management Dashboard."""
    status_filter = request.args.get("status")
    industry_filter = request.args.get("industry")
    search_query = request.args.get("search")

    query = Quotation.query.join(Project).join(Customer)

    if status_filter:
        query = query.filter(Quotation.status == status_filter)
    if industry_filter:
        query = query.filter(Project.industry.ilike(f"%{industry_filter}%"))
    if search_query:
        query = query.filter(
            (Quotation.reference_no.ilike(f"%{search_query}%")) |
            (Customer.name.ilike(f"%{search_query}%")) |
            (Customer.company.ilike(f"%{search_query}%")) |
            (Project.name.ilike(f"%{search_query}%"))
        )

    all_quotations = query.order_by(Quotation.created_at.desc()).all()
    
    # Calculate quick metrics
    total_pipeline_val = sum(q.total_cost for q in all_quotations)
    approved_val = sum(q.total_cost for q in all_quotations if q.status == "Approved")
    draft_count = sum(1 for q in all_quotations if q.status == "Draft")
    approved_count = sum(1 for q in all_quotations if q.status == "Approved")

    return render_template(
        "quotations.html",
        quotations=all_quotations,
        total_count=len(all_quotations),
        total_pipeline_val=total_pipeline_val,
        approved_val=approved_val,
        draft_count=draft_count,
        approved_count=approved_count,
        status_filter=status_filter,
        industry_filter=industry_filter,
        search_query=search_query,
        db_type=app.config.get("DB_ENGINE_TYPE", "SQLite")
    )


@app.route("/quotations/<int:quotation_id>")
def view_quotation(quotation_id):
    """Detailed single quotation view with versions and audit log."""
    quotation = Quotation.query.get_or_404(quotation_id)
    version_id = request.args.get("version_id", type=int)

    selected_version = None
    if version_id:
        selected_version = QuotationVersion.query.filter_by(quotation_id=quotation.id, id=version_id).first()
    if not selected_version and quotation.versions:
        selected_version = quotation.versions[0]

    version_data = selected_version.get_data() if selected_version else {}
    activities = ActivityLog.query.filter_by(quotation_id=quotation.id).order_by(ActivityLog.timestamp.desc()).all()

    return render_template(
        "view_quotation.html",
        quotation=quotation,
        selected_version=selected_version,
        data=version_data,
        activities=activities,
        db_type=app.config.get("DB_ENGINE_TYPE", "SQLite")
    )


@app.route("/settings")
def settings_page():
    """System Diagnostics and API Configurations."""
    return render_template(
        "settings.html",
        has_gemini_key=bool(Config.GEMINI_API_KEY),
        gemini_model=Config.GEMINI_MODEL,
        db_type=app.config.get("DB_ENGINE_TYPE", "SQLite"),
        db_uri=Config.get_database_uri().split("@")[-1] if "@" in Config.get_database_uri() else Config.get_database_uri(),
        company_name=Config.COMPANY_NAME,
        company_email=Config.COMPANY_EMAIL,
        company_website=Config.COMPANY_WEBSITE,
        default_tax=int(Config.DEFAULT_TAX_RATE * 100),
        default_contingency=int(Config.DEFAULT_CONTINGENCY * 100)
    )


# -------------------------------------------------------------
# REST API ENDPOINTS
# -------------------------------------------------------------

@app.route("/api/samples", methods=["GET"])
def get_samples():
    """Returns the list of industry sample emails."""
    return jsonify({"status": "success", "samples": SAMPLE_EMAILS})


@app.route("/api/analyze-email", methods=["POST"])
def api_analyze_email():
    """
    Accepts customer email text and runs Gemini analysis.
    Extracts industry, requirements, assumptions, questions, and complexity.
    """
    data = request.get_json() or {}
    email_text = data.get("email_text", "").strip()
    custom_api_key = data.get("gemini_api_key", "").strip() or None

    if not email_text:
        return jsonify({"status": "error", "message": "Email text cannot be empty."}), 400

    try:
        analysis_result = analyze_email_with_gemini(email_text, custom_api_key=custom_api_key)
        return jsonify({
            "status": "success",
            "analysis": analysis_result
        })
    except Exception as e:
        logger.exception("Email analysis failed")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/estimate", methods=["POST"])
def api_estimate():
    """
    Computes deterministic Python estimates from analysis data and custom overrides.
    """
    data = request.get_json() or {}
    analysis_data = data.get("analysis")
    custom_overrides = data.get("custom_overrides", {})

    if not analysis_data:
        return jsonify({"status": "error", "message": "Missing analysis data for estimation."}), 400

    try:
        estimates = calculate_project_estimates(analysis_data, custom_overrides)
        return jsonify({
            "status": "success",
            "estimates": estimates
        })
    except Exception as e:
        logger.exception("Estimation failed")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/quotations/create", methods=["POST"])
def api_create_quotation():
    """
    Persists customer, project, quotation, and initial version (v1) in MySQL/SQLAlchemy.
    Generates the executive PDF file and returns details.
    """
    payload = request.get_json() or {}
    analysis = payload.get("analysis")
    estimates = payload.get("estimates")
    email_source = payload.get("email_source", "")

    if not analysis or not estimates:
        return jsonify({"status": "error", "message": "Both analysis and estimates are required."}), 400

    try:
        cust_info = analysis.get("customer", {})
        proj_info = analysis.get("project_title", "Enterprise Solution")
        ind_info = analysis.get("industry", {})
        industry_name = ind_info.get("industry_name", "General")
        category_name = ind_info.get("category", "Custom Solution")
        comp_info = analysis.get("complexity", {})

        # 1. Save or find Customer
        customer_email = cust_info.get("email", "client@example.com")
        customer = Customer.query.filter_by(email=customer_email).first()
        if not customer:
            customer = Customer(
                name=cust_info.get("name", "Prospective Client"),
                email=customer_email,
                company=cust_info.get("company", "Client Organization"),
                phone=cust_info.get("phone", "N/A"),
                address=""
            )
            db.session.add(customer)
            db.session.flush()

        # 2. Save Project
        project = Project(
            customer_id=customer.id,
            name=proj_info,
            industry=industry_name,
            category=category_name,
            complexity=comp_info.get("level", "Medium"),
            complexity_score=comp_info.get("score", 50),
            business_objectives=analysis.get("business_objectives", ""),
            email_source_text=email_source
        )
        db.session.add(project)
        db.session.flush()

        # 3. Create Quotation Master
        ref_no = generate_reference_number(industry_name)
        grand_total = estimates.get("cost_breakdown", {}).get("grand_total", 0.0)

        quotation = Quotation(
            reference_no=ref_no,
            project_id=project.id,
            current_version=1,
            status="Draft",
            total_cost=grand_total,
            currency="INR"
        )
        db.session.add(quotation)
        db.session.flush()

        # 4. Generate Professional PDF Quotation
        pdf_path = generate_quotation_pdf(
            quotation_ref=ref_no,
            analysis_data=analysis,
            estimation_data=estimates,
            version_num=1,
            status="Draft"
        )

        # 5. Save Quotation Version 1
        combined_data = {
            "analysis": analysis,
            "estimates": estimates,
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "reference_no": ref_no,
                "version": 1
            }
        }
        quotation_ver = QuotationVersion(
            quotation_id=quotation.id,
            version_number=1,
            status="Draft",
            pdf_path=pdf_path,
            notes="Initial AI quotation generated from email intake analysis."
        )
        quotation_ver.set_data(combined_data)
        db.session.add(quotation_ver)

        # 6. Log Activity
        activity = ActivityLog(
            quotation_id=quotation.id,
            action="Quotation Generated (v1)",
            details=f"Analyzed customer inquiry from {customer.name} ({customer.company}). Auto-detected industry: {industry_name}. Estimated investment: {format_inr(grand_total)} INR."
        )
        db.session.add(activity)

        db.session.commit()

        logger.info(f"Quotation {ref_no} (v1) created successfully.")

        return jsonify({
            "status": "success",
            "quotation_id": quotation.id,
            "reference_no": ref_no,
            "version": 1,
            "total_cost": grand_total,
            "total_cost_formatted": format_inr(grand_total),
            "currency": "INR",
            "pdf_url": f"/api/quotations/{quotation.id}/pdf",
            "preview_url": f"/api/quotations/{quotation.id}/pdf/preview"
        })

    except Exception as e:
        db.session.rollback()
        logger.exception("Failed to create quotation")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/quotations/<int:quotation_id>/revise", methods=["POST"])
def api_revise_quotation(quotation_id):
    """
    Creates a new revision (v2, v3...) for an existing quotation with modified estimates or notes.
    """
    quotation = Quotation.query.get_or_404(quotation_id)
    payload = request.get_json() or {}
    
    revised_estimates = payload.get("estimates")
    revision_notes = payload.get("notes", "Revised estimates after client review.")

    if not revised_estimates:
        return jsonify({"status": "error", "message": "Revised estimates are required."}), 400

    try:
        latest_ver = quotation.versions[0] if quotation.versions else None
        current_data = latest_ver.get_data() if latest_ver else {}
        analysis = current_data.get("analysis", {})

        new_version_num = quotation.current_version + 1
        quotation.current_version = new_version_num
        quotation.status = "Revised"
        
        new_total = revised_estimates.get("cost_breakdown", {}).get("grand_total", quotation.total_cost)
        quotation.total_cost = new_total

        # Re-generate PDF with updated version
        pdf_path = generate_quotation_pdf(
            quotation_ref=quotation.reference_no,
            analysis_data=analysis,
            estimation_data=revised_estimates,
            version_num=new_version_num,
            status="Revised"
        )

        combined_data = {
            "analysis": analysis,
            "estimates": revised_estimates,
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "reference_no": quotation.reference_no,
                "version": new_version_num
            }
        }

        new_ver = QuotationVersion(
            quotation_id=quotation.id,
            version_number=new_version_num,
            status="Revised",
            pdf_path=pdf_path,
            notes=revision_notes
        )
        new_ver.set_data(combined_data)
        db.session.add(new_ver)

        activity = ActivityLog(
            quotation_id=quotation.id,
            action=f"Quotation Revised to v{new_version_num}",
            details=f"Updated estimates. New total: {format_inr(new_total)} INR. Notes: {revision_notes}"
        )
        db.session.add(activity)

        db.session.commit()

        return jsonify({
            "status": "success",
            "quotation_id": quotation.id,
            "version": new_version_num,
            "total_cost": new_total,
            "total_cost_formatted": format_inr(new_total),
            "currency": "INR",
            "pdf_url": f"/api/quotations/{quotation.id}/pdf?version={new_version_num}"
        })

    except Exception as e:
        db.session.rollback()
        logger.exception("Failed to revise quotation")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/quotations/<int:quotation_id>/status", methods=["POST"])
def api_update_status(quotation_id):
    """Updates the status of a quotation (Draft, In Review, Approved, Sent, Rejected)."""
    quotation = Quotation.query.get_or_404(quotation_id)
    payload = request.get_json() or {}
    new_status = payload.get("status")

    valid_statuses = ["Draft", "In Review", "Approved", "Sent", "Revised", "Rejected"]
    if new_status not in valid_statuses:
        return jsonify({"status": "error", "message": f"Invalid status. Choose from: {valid_statuses}"}), 400

    try:
        old_status = quotation.status
        quotation.status = new_status
        
        # Also update latest version status
        if quotation.versions:
            quotation.versions[0].status = new_status

        activity = ActivityLog(
            quotation_id=quotation.id,
            action=f"Status Changed: {old_status} -> {new_status}",
            details=f"User updated quotation status to {new_status}."
        )
        db.session.add(activity)
        db.session.commit()

        return jsonify({"status": "success", "status_updated": new_status})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/quotations/<int:quotation_id>/pdf", methods=["GET"])
def api_download_pdf(quotation_id):
    """Direct PDF file download endpoint."""
    quotation = Quotation.query.get_or_404(quotation_id)
    version_num = request.args.get("version", type=int)

    ver = None
    if version_num:
        ver = QuotationVersion.query.filter_by(quotation_id=quotation.id, version_number=version_num).first()
    if not ver and quotation.versions:
        ver = quotation.versions[0]

    if not ver or not ver.pdf_path or not os.path.exists(ver.pdf_path):
        return jsonify({"status": "error", "message": "PDF file not found."}), 404

    filename = os.path.basename(ver.pdf_path)
    return send_file(ver.pdf_path, as_attachment=True, download_name=filename, mimetype="application/pdf")


@app.route("/api/quotations/<int:quotation_id>/pdf/preview", methods=["GET"])
def api_preview_pdf(quotation_id):
    """In-browser PDF preview endpoint (inline disposition)."""
    quotation = Quotation.query.get_or_404(quotation_id)
    version_num = request.args.get("version", type=int)

    ver = None
    if version_num:
        ver = QuotationVersion.query.filter_by(quotation_id=quotation.id, version_number=version_num).first()
    if not ver and quotation.versions:
        ver = quotation.versions[0]

    if not ver or not ver.pdf_path or not os.path.exists(ver.pdf_path):
        return jsonify({"status": "error", "message": "PDF file not found."}), 404

    return send_file(ver.pdf_path, as_attachment=False, mimetype="application/pdf")


@app.route("/api/test-gemini", methods=["POST"])
def api_test_gemini():
    """Validates connectivity to Google Gemini API."""
    payload = request.get_json() or {}
    api_key = payload.get("api_key", "").strip() or Config.GEMINI_API_KEY

    if not api_key:
        return jsonify({"status": "error", "message": "No API key provided to test."}), 400

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        resp = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents="Respond with the single word: OK"
        )
        return jsonify({
            "status": "success",
            "message": "Gemini API connection verified successfully!",
            "response": resp.text.strip()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gemini connection failed: {str(e)}"
        }), 400


# -------------------------------------------------------------
# APPLICATION ENTRYPOINT
# -------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    logger.info(f"Starting QuoteFlow on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)

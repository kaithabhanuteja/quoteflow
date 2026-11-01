"""
Comprehensive Unit and Integration Test Suite for QuoteFlow.
Tests industry detection, requirement parsing, estimation logic, PDF generation,
and Flask REST API endpoints.
"""

import os
import unittest
import json
from app import app, db
from models import Customer, Project, Quotation, QuotationVersion, ActivityLog
from services import (
    SAMPLE_EMAILS,
    analyze_email_with_gemini,
    calculate_project_estimates,
    generate_quotation_pdf,
    get_industry_profile
)

class QuoteFlowTestSuite(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_sample_emails_exist(self):
        """Verify sample emails cover multiple industries."""
        self.assertGreaterEqual(len(SAMPLE_EMAILS), 5)
        titles = [s["title"] for s in SAMPLE_EMAILS]
        self.assertTrue(any("Healthcare" in t for t in titles))
        self.assertTrue(any("FinTech" in t for t in titles))
        self.assertTrue(any("Logistics" in t for t in titles))

    def test_automatic_industry_detection_healthcare(self):
        """Ensure automatic detection of Healthcare without any manual selection."""
        healthcare_email = SAMPLE_EMAILS[0]["body"]
        result = analyze_email_with_gemini(healthcare_email)
        
        self.assertEqual(result["industry"]["industry_name"], "Healthcare & MedTech")
        self.assertGreater(result["industry"]["confidence_score"], 70)
        self.assertEqual(result["customer"]["company"], "Apex Health Group")
        self.assertIn("Dr. Sarah Jenkins", result["customer"]["name"])

    def test_automatic_industry_detection_fintech(self):
        """Ensure automatic detection of FinTech & Banking."""
        fintech_email = SAMPLE_EMAILS[1]["body"]
        result = analyze_email_with_gemini(fintech_email)
        
        self.assertEqual(result["industry"]["industry_name"], "FinTech & Banking")
        self.assertEqual(result["customer"]["company"], "Apex Capital Partners")

    def test_automatic_industry_detection_custom_unknown(self):
        """Ensure dynamic handling of unknown / custom industries (Precision AgTech Drone)."""
        agtech_email = SAMPLE_EMAILS[5]["body"]
        result = analyze_email_with_gemini(agtech_email)
        
        self.assertIn("Agriculture", result["industry"]["industry_name"])
        profile = get_industry_profile(result["industry"]["industry_name"])
        self.assertIsNotNone(profile)
        self.assertTrue(len(profile["key_deliverables"]) > 0)

    def test_confirmed_vs_assumptions_distinction(self):
        """Ensure confirmed requirements and AI assumptions are cleanly differentiated."""
        healthcare_email = SAMPLE_EMAILS[0]["body"]
        result = analyze_email_with_gemini(healthcare_email)
        
        reqs = result["requirements"]
        confirmed = [r for r in reqs if r["is_confirmed"]]
        assumed = [r for r in reqs if not r["is_confirmed"]]
        
        self.assertGreater(len(confirmed), 0, "Must have confirmed requirements from email")
        self.assertGreater(len(assumed), 0, "Must distinguish AI-derived assumptions")

    def test_clarification_questions_generation(self):
        """Ensure clarification questions are formulated for missing details."""
        email = SAMPLE_EMAILS[0]["body"]
        result = analyze_email_with_gemini(email)
        
        questions = result["clarification_questions"]
        self.assertGreaterEqual(len(questions), 2)
        for q in questions:
            self.assertTrue(bool(q["question"]))
            self.assertTrue(bool(q["why_needed"]))
            self.assertTrue(bool(q["suggested_default"]))

    def test_deterministic_cost_estimation(self):
        """Verify deterministic mathematical calculation of effort, taxes, and grand total."""
        email = SAMPLE_EMAILS[0]["body"]
        analysis = analyze_email_with_gemini(email)
        estimates = calculate_project_estimates(analysis)
        
        costs = estimates["cost_breakdown"]
        subtotal = costs["subtotal"]
        contingency = costs["contingency_cost"]
        tax = costs["tax_cost"]
        grand_total = costs["grand_total"]
        
        # Verify subtotal equals sum of parts
        calc_subtotal = round(
            costs["development_cost"] + costs["integration_cost"] + costs["design_cost"] +
            costs["qa_testing_cost"] + costs["devops_cloud_cost"] + costs["project_management_cost"] +
            costs["architecture_cost"] + costs["compliance_cost"] + costs["infrastructure_staging_cost"], 
            2
        )
        self.assertAlmostEqual(subtotal, calc_subtotal, delta=1.0)
        
        # Verify contingency = 10%
        expected_contingency = round(subtotal * 0.10, 2)
        self.assertAlmostEqual(contingency, expected_contingency, delta=1.0)
        
        # Verify tax = 18% of taxable amount
        expected_tax = round((subtotal + contingency) * 0.18, 2)
        self.assertAlmostEqual(tax, expected_tax, delta=1.0)
        
        # Verify grand total
        self.assertAlmostEqual(grand_total, subtotal + contingency + tax, delta=1.0)

        # Verify payment milestones sum to grand total
        milestone_sum = sum(m["amount"] for m in estimates["payment_milestones"])
        self.assertAlmostEqual(milestone_sum, grand_total, delta=0.5)

    def test_pdf_generation_flow(self):
        """Ensure multi-page executive PDF is generated on disk."""
        email = SAMPLE_EMAILS[0]["body"]
        analysis = analyze_email_with_gemini(email)
        estimates = calculate_project_estimates(analysis)
        
        ref_no = "QF-TEST-UNIT-9999"
        pdf_path = generate_quotation_pdf(ref_no, analysis, estimates, version_num=1, status="Draft")
        
        self.assertTrue(os.path.exists(pdf_path))
        self.assertGreater(os.path.getsize(pdf_path), 5000)

    def test_indian_rupee_formatting(self):
        """Verify Indian comma grouping format for ₹1,50,000 and ₹12,50,000."""
        from services import format_inr
        self.assertEqual(format_inr(150000, decimals=0), "₹1,50,000")
        self.assertEqual(format_inr(1250000, decimals=0), "₹12,50,000")
        self.assertEqual(format_inr(150000.00), "₹1,50,000.00")
        self.assertEqual(format_inr(1250000.50), "₹12,50,000.50")
        self.assertEqual(format_inr(265875.83), "₹2,65,875.83")

    def test_company_and_developer_metadata(self):
        """Verify developer name Kaitha Bhanuteja and company Quotflow Technologies Limited."""
        from config import Config
        self.assertEqual(Config.DEVELOPER_NAME, "Kaitha Bhanuteja")
        self.assertEqual(Config.COMPANY_NAME, "Quotflow Technologies Limited")
        self.assertIn("Hyderabad", Config.COMPANY_ADDRESS)
        self.assertEqual(Config.DEFAULT_CURRENCY, "INR")

    def test_api_quotation_lifecycle(self):
        """Test full REST API lifecycle: analyze -> estimate -> create -> revise -> status -> get PDF."""
        # 1. Analyze Email
        resp = self.client.post("/api/analyze-email", json={
            "email_text": SAMPLE_EMAILS[0]["body"]
        })
        self.assertEqual(resp.status_code, 200)
        analysis_data = resp.get_json()["analysis"]

        # 2. Estimate
        resp2 = self.client.post("/api/estimate", json={
            "analysis": analysis_data
        })
        self.assertEqual(resp2.status_code, 200)
        estimate_data = resp2.get_json()["estimates"]

        # 3. Create Quotation in Database
        resp3 = self.client.post("/api/quotations/create", json={
            "analysis": analysis_data,
            "estimates": estimate_data,
            "email_source": SAMPLE_EMAILS[0]["body"]
        })
        self.assertEqual(resp3.status_code, 200)
        created = resp3.get_json()
        quote_id = created["quotation_id"]
        ref_no = created["reference_no"]

        # 4. Check Database records
        with app.app_context():
            q = db.session.get(Quotation, quote_id)
            self.assertIsNotNone(q)
            self.assertEqual(q.reference_no, ref_no)
            self.assertEqual(q.current_version, 1)
            self.assertEqual(len(q.versions), 1)

        # 5. Revise Quotation to v2
        resp4 = self.client.post(f"/api/quotations/{quote_id}/revise", json={
            "estimates": estimate_data,
            "notes": "Client requested updated milestone split."
        })
        self.assertEqual(resp4.status_code, 200)
        self.assertEqual(resp4.get_json()["version"], 2)

        # 6. Update Status to Approved
        resp5 = self.client.post(f"/api/quotations/{quote_id}/status", json={
            "status": "Approved"
        })
        self.assertEqual(resp5.status_code, 200)

        with app.app_context():
            q = db.session.get(Quotation, quote_id)
            self.assertEqual(q.status, "Approved")
            self.assertEqual(q.current_version, 2)

        # 7. Fetch PDF download
        pdf_resp = self.client.get(f"/api/quotations/{quote_id}/pdf")
        self.assertEqual(pdf_resp.status_code, 200)
        self.assertEqual(pdf_resp.mimetype, "application/pdf")

if __name__ == "__main__":
    unittest.main()

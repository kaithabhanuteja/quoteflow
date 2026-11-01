"""
Executive-Grade ReportLab PDF Quotation Generator for Quotflow.
Generates multi-page, beautifully styled quotation documents with dynamic industry styling,
page numbering (Page X of Y), detailed financial tables with Indian Rupee formatting (₹),
and authorized sign-off blocks.
"""

import os
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import Config
from services.industry_config import get_industry_profile
from services.estimator import format_inr

logger = logging.getLogger(__name__)

# Register Unicode TrueType Font to flawlessly render Indian Rupee (₹) symbol
PDF_FONT_REGULAR = "Helvetica"
PDF_FONT_BOLD = "Helvetica-Bold"

try:
    font_candidates = [
        ("SegoeUI", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf"),
        ("Arial", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
        ("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    ]
    for font_family, reg_path, bold_path in font_candidates:
        if os.path.exists(reg_path) and os.path.exists(bold_path):
            pdfmetrics.registerFont(TTFont(font_family, reg_path))
            pdfmetrics.registerFont(TTFont(f"{font_family}-Bold", bold_path))
            PDF_FONT_REGULAR = font_family
            PDF_FONT_BOLD = f"{font_family}-Bold"
            logger.info(f"Registered TrueType font for PDF: {font_family}")
            break
except Exception as e:
    logger.warning(f"Could not register custom TrueType font, using standard fallback: {e}")


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page counts
    e.g. 'Page 1 of 5' along with running header and footer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont(PDF_FONT_REGULAR, 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Footer
        footer_y = 30
        self.drawString(
            54, footer_y,
            f"Quotflow Confidential | Generated on {datetime.now().strftime('%B %d, %Y')} | Quotation Reference Document"
        )
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, footer_y, page_str)
        
        # Subtle footer divider
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, footer_y + 12, letter[0] - 54, footer_y + 12)

        # Header for pages > 1
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Quotflow Technologies Limited | Formal Commercial Quotation")
            self.drawRightString(letter[0] - 54, letter[1] - 36, f"Ref: {getattr(self, 'ref_no', 'QUOTATION')}")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        self.restoreState()


def generate_quotation_pdf(
    quotation_ref: str,
    analysis_data: Dict[str, Any],
    estimation_data: Dict[str, Any],
    version_num: int = 1,
    status: str = "Draft"
) -> str:
    """
    Builds the complete executive quotation PDF and saves to storage.
    Returns the absolute path to the generated PDF.
    """
    filename = f"{quotation_ref}_v{version_num}.pdf".replace("/", "_").replace(" ", "_")
    output_path = Config.STORAGE_DIR / filename

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    # Industry-specific color scheme
    industry_info = analysis_data.get("industry", {})
    industry_name = industry_info.get("industry_name", "General")
    profile = get_industry_profile(industry_name)
    primary_hex = profile.get("badge_color", "#1e3a8a")
    accent_hex = profile.get("accent_color", "#2563eb")
    
    c_primary = colors.HexColor(primary_hex)
    c_accent = colors.HexColor(accent_hex)
    c_dark = colors.HexColor("#0f172a")
    c_slate = colors.HexColor("#334155")
    c_muted = colors.HexColor("#64748b")
    c_light = colors.HexColor("#f8fafc")
    c_border = colors.HexColor("#e2e8f0")
    c_success = colors.HexColor("#16a34a")
    c_warning = colors.HexColor("#d97706")

    # Typography Styles using custom or standard fonts
    styles = getSampleStyleSheet()
    
    style_h1 = ParagraphStyle(
        "PDF_H1",
        parent=styles["Heading1"],
        fontName=PDF_FONT_BOLD,
        fontSize=18,
        leading=22,
        textColor=c_dark,
        spaceAfter=4
    )
    
    style_h2 = ParagraphStyle(
        "PDF_H2",
        parent=styles["Heading2"],
        fontName=PDF_FONT_BOLD,
        fontSize=12,
        leading=16,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6
    )

    style_h3 = ParagraphStyle(
        "PDF_H3",
        parent=styles["Heading3"],
        fontName=PDF_FONT_BOLD,
        fontSize=10,
        leading=14,
        textColor=c_dark,
        spaceBefore=6,
        spaceAfter=3
    )

    style_body = ParagraphStyle(
        "PDF_Body",
        parent=styles["Normal"],
        fontName=PDF_FONT_REGULAR,
        fontSize=8.5,
        leading=12,
        textColor=c_slate
    )

    style_body_bold = ParagraphStyle(
        "PDF_BodyBold",
        parent=style_body,
        fontName=PDF_FONT_BOLD,
        textColor=c_dark
    )

    style_small = ParagraphStyle(
        "PDF_Small",
        parent=styles["Normal"],
        fontName=PDF_FONT_REGULAR,
        fontSize=7.5,
        leading=10.5,
        textColor=c_muted
    )

    style_tag_confirmed = ParagraphStyle(
        "PDF_TagConfirmed",
        parent=styles["Normal"],
        fontName=PDF_FONT_BOLD,
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#15803d")
    )

    style_tag_assumption = ParagraphStyle(
        "PDF_TagAssumption",
        parent=styles["Normal"],
        fontName=PDF_FONT_BOLD,
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#b45309")
    )

    story = []
    page_width = letter[0] - 108  # Printable width = 504 pt

    # 1. HEADER SECTION: Company Branding & Quotation Metadata
    header_data = [
        [
            Paragraph(
                f"<b><font size=16 color='{primary_hex}'>Quotflow</font></b><br/>"
                f"<font size=8 color='#64748b'><b>QUOTFLOW TECHNOLOGIES LIMITED</b><br/>"
                f"{Config.COMPANY_ADDRESS}<br/>"
                f"Web: {Config.COMPANY_WEBSITE} | Email: {Config.COMPANY_EMAIL}<br/>"
                f"Tax / GST: {Config.COMPANY_TAX_ID}</font>",
                style_body
            ),
            Paragraph(
                f"<div align='right'>"
                f"<b><font size=12 color='{primary_hex}'>COMMERCIAL QUOTATION</font></b><br/>"
                f"<font size=8><b>Ref No:</b> {quotation_ref}</font><br/>"
                f"<font size=8><b>Date:</b> {datetime.now().strftime('%B %d, %Y')}</font><br/>"
                f"<font size=8><b>Valid Until:</b> {(datetime.now() + timedelta(days=Config.DEFAULT_VALIDITY_DAYS)).strftime('%B %d, %Y')}</font><br/>"
                f"<font size=8><b>Version:</b> v{version_num} | <b>Status:</b> {status.upper()}</font>"
                f"</div>",
                style_body
            )
        ]
    ]
    t_header = Table(header_data, colWidths=[page_width * 0.55, page_width * 0.45])
    t_header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t_header)

    # Divider bar in primary brand color
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=4, spaceAfter=10))

    # 2. CLIENT & PROJECT METADATA CARD
    cust = analysis_data.get("customer", {})
    client_box = [
        [
            Paragraph(f"<b>PREPARED FOR:</b><br/>"
                      f"<b>{cust.get('name', 'Prospective Client')}</b><br/>"
                      f"{cust.get('designation', 'Lead Stakeholder')}<br/>"
                      f"<b>{cust.get('company', 'Client Organization')}</b><br/>"
                      f"Email: {cust.get('email', 'N/A')}<br/>"
                      f"Phone: {cust.get('phone', 'N/A')}", style_body),
            Paragraph(f"<b>PROJECT & ENGAGEMENT:</b><br/>"
                      f"<b>Project:</b> {analysis_data.get('project_title', 'Enterprise Solution')}<br/>"
                      f"<b>Detected Industry:</b> {industry_name}<br/>"
                      f"<b>Domain Category:</b> {industry_info.get('category', 'Custom Solution')}<br/>"
                      f"<b>Complexity Evaluation:</b> {estimation_data.get('complexity_level', 'Medium')} ({estimation_data.get('complexity_score', 50)}/100)<br/>"
                      f"<b>Currency / Terms:</b> INR (₹) | Net-30 Milestones", style_body)
        ]
    ]
    t_client = Table(client_box, colWidths=[page_width * 0.5, page_width * 0.5])
    t_client.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(profile.get("bg_soft", "#f8fafc"))),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_client)
    story.append(Spacer(1, 12))

    # 3. EXECUTIVE SUMMARY & BUSINESS OBJECTIVES
    story.append(Paragraph("1. Executive Summary & Business Objectives", style_h2))
    story.append(Paragraph(
        f"{analysis_data.get('business_objectives', 'Deliver a highly reliable, industry-grade software solution tailored to client requirements.')}",
        style_body
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"<b>Industry Alignment & Compliance:</b> This engagement has been automatically mapped to our <b>{industry_name}</b> "
        f"engineering practice. All architecture deliverables and deployment topologies will strictly adhere to: "
        f"<i>{', '.join(profile.get('compliance_standards', ['Standard SOC-2 Guidelines'])[:3])}</i>.",
        style_body
    ))
    story.append(Spacer(1, 10))

    # 4. SCOPE OF WORK & REQUIREMENTS MATRIX (Confirmed vs Assumptions)
    story.append(Paragraph("2. Scope of Work & Requirements Breakdown", style_h2))
    story.append(Paragraph(
        "To ensure total transparency, all requirements have been classified into <b>[Confirmed]</b> (verbatim from customer inquiry) "
        "and <b>[AI Assumption]</b> (best-practice inferences incorporated for an accurate estimate).",
        style_small
    ))
    story.append(Spacer(1, 6))

    reqs = analysis_data.get("requirements", [])
    req_rows = [
        [
            Paragraph("<b>Code</b>", style_body_bold),
            Paragraph("<b>Classification</b>", style_body_bold),
            Paragraph("<b>Requirement & Scope of Deliverable</b>", style_body_bold),
            Paragraph("<b>Category</b>", style_body_bold),
        ]
    ]
    for r in reqs[:8]:  # Top 8 comprehensive items
        is_conf = r.get("is_confirmed", True)
        badge = Paragraph("<font color='#16a34a'><b>CONFIRMED</b></font>", style_tag_confirmed) if is_conf else Paragraph("<font color='#d97706'><b>AI ASSUMPTION</b></font>", style_tag_assumption)
        desc_text = f"<b>{r.get('title', 'Feature')}</b>: {r.get('description', '')}"
        req_rows.append([
            Paragraph(r.get("id", "REQ"), style_body),
            badge,
            Paragraph(desc_text, style_body),
            Paragraph(r.get("category", "Functional"), style_body)
        ])

    t_reqs = Table(req_rows, colWidths=[page_width * 0.12, page_width * 0.18, page_width * 0.55, page_width * 0.15])
    t_reqs.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_light])
    ]))
    story.append(t_reqs)
    story.append(Spacer(1, 10))

    # 5. INDUSTRY-SPECIFIC DELIVERABLES & REGULATORY STANDARDS
    story.append(Paragraph(f"3. {industry_name} Specialized Deliverables & Standards", style_h2))
    ind_deliverables = profile.get("key_deliverables", [])
    ind_standards = profile.get("compliance_standards", [])
    
    ind_data = [
        [
            Paragraph("<b>Industry Deliverable Specifications</b>", style_body_bold),
            Paragraph("<b>Regulatory & Quality Standards</b>", style_body_bold)
        ],
        [
            Paragraph("<br/>".join([f"• {d}" for d in ind_deliverables[:5]]), style_body),
            Paragraph("<br/>".join([f"• {s}" for s in ind_standards[:5]]), style_body)
        ]
    ]
    t_ind = Table(ind_data, colWidths=[page_width * 0.55, page_width * 0.45])
    t_ind.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_ind)
    story.append(Spacer(1, 12))

    # 6. CLARIFICATION QUESTIONS FOR CUSTOMER REVIEW
    clarifications = analysis_data.get("clarification_questions", [])
    if clarifications:
        story.append(Paragraph("4. Key Information Clarifications (Pre-Kickoff Alignment)", style_h2))
        story.append(Paragraph(
            "The following open questions were identified during automated intake analysis. "
            "Resolving these items will confirm precision before Sprint 0 finalization:",
            style_small
        ))
        story.append(Spacer(1, 4))
        
        q_rows = [
            [
                Paragraph("<b>No.</b>", style_body_bold),
                Paragraph("<b>Clarification Question</b>", style_body_bold),
                Paragraph("<b>Suggested Baseline Assumption</b>", style_body_bold)
            ]
        ]
        for q in clarifications[:4]:
            q_rows.append([
                Paragraph(q.get("id", "QST"), style_body),
                Paragraph(f"<b>{q.get('question', '')}</b><br/><font color='#64748b' size=7.5>Impact: {q.get('why_needed', '')}</font>", style_body),
                Paragraph(q.get("suggested_default", "Standard enterprise implementation."), style_body)
            ])
        t_q = Table(q_rows, colWidths=[page_width * 0.10, page_width * 0.52, page_width * 0.38])
        t_q.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ("BOX", (0, 0), (-1, -1), 0.5, c_border),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_light])
        ]))
        story.append(t_q)
        story.append(Spacer(1, 12))

    # PAGE BREAK FOR FINANCIALS & TIMELINE TO KEEP THEM PRISTINE TOGETHER
    story.append(PageBreak())

    # 7. IMPLEMENTATION PHASES & DELIVERY ROADMAP
    story.append(Paragraph("5. Project Implementation Roadmap & Phase Schedule", style_h2))
    phases = estimation_data.get("phases", [])
    phase_rows = [
        [
            Paragraph("<b>Phase & Description</b>", style_body_bold),
            Paragraph("<b>Hours</b>", style_body_bold),
            Paragraph("<b>Duration</b>", style_body_bold),
            Paragraph("<b>Key Milestones & Deliverables</b>", style_body_bold)
        ]
    ]
    for ph in phases:
        dels = ph.get("deliverables", [])
        del_text = "<br/>".join([f"• {d}" for d in dels[:2]])
        phase_rows.append([
            Paragraph(f"<b>{ph.get('name', 'Phase')}</b>", style_body),
            Paragraph(f"{ph.get('hours', 0)} hrs", style_body),
            Paragraph(f"{ph.get('weeks', 1)} wks", style_body),
            Paragraph(del_text, style_body)
        ])
    t_phases = Table(phase_rows, colWidths=[page_width * 0.36, page_width * 0.12, page_width * 0.12, page_width * 0.40])
    t_phases.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_light])
    ]))
    story.append(t_phases)
    story.append(Spacer(1, 12))

    # 8. RESOURCE ALLOCATION & TEAM ALLOCATION
    story.append(Paragraph("6. Resource Allocation & Team Composition", style_h2))
    team = estimation_data.get("team_allocation", [])
    team_rows = [
        [
            Paragraph("<b>Role & Title</b>", style_body_bold),
            Paragraph("<b>Seniority</b>", style_body_bold),
            Paragraph("<b>Staff</b>", style_body_bold),
            Paragraph("<b>Hours</b>", style_body_bold),
            Paragraph("<b>Rate/Hr</b>", style_body_bold),
            Paragraph("<b>Total Cost</b>", style_body_bold),
        ]
    ]
    for m in team:
        team_rows.append([
            Paragraph(f"<b>{m.get('role')}</b>", style_body),
            Paragraph(m.get("seniority", "Senior"), style_body),
            Paragraph(str(m.get("headcount", 1)), style_body),
            Paragraph(f"{m.get('hours', 0)}", style_body),
            Paragraph(f"{format_inr(m.get('rate', 0.0))}/hr", style_body),
            Paragraph(f"{format_inr(m.get('cost', 0.0))}", style_body_bold),
        ])
    t_team = Table(team_rows, colWidths=[page_width * 0.34, page_width * 0.20, page_width * 0.08, page_width * 0.10, page_width * 0.12, page_width * 0.16])
    t_team.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_light])
    ]))
    story.append(t_team)
    story.append(Spacer(1, 12))

    # 9. ITEMIZED FINANCIAL SUMMARY & COST BREAKDOWN (INR FORMATTING)
    costs = estimation_data.get("cost_breakdown", {})
    subtotal = costs.get("subtotal", 0.0)
    contingency = costs.get("contingency_cost", 0.0)
    contingency_pct = int(costs.get("contingency_percentage", 0.10) * 100)
    tax = costs.get("tax_cost", 0.0)
    tax_pct = int(costs.get("tax_percentage", 0.18) * 100)
    discount = costs.get("discount_amount", 0.0)
    grand_total = costs.get("grand_total", 0.0)

    story.append(Paragraph("7. Detailed Item-Wise Commercial Quotation", style_h2))
    
    financial_rows = [
        [Paragraph("<b>Item / Cost Component</b>", style_body_bold), Paragraph("<b>Detailed Description</b>", style_body_bold), Paragraph("<b>Subtotal (INR)</b>", style_body_bold)],
        [Paragraph("Core Software Development", style_body), Paragraph("Senior and Mid full-stack engineering effort across core business logic", style_body), Paragraph(f"{format_inr(costs.get('development_cost', 0.0))}", style_body)],
        [Paragraph("Third-Party Integrations & Middleware", style_body), Paragraph("Enterprise connectors, webhooks, data pipelines, error isolation", style_body), Paragraph(f"{format_inr(costs.get('integration_cost', 0.0))}", style_body)],
        [Paragraph("UI/UX & Interactive Design System", style_body), Paragraph("Figma design system, component tokens, accessibility compliance", style_body), Paragraph(f"{format_inr(costs.get('design_cost', 0.0))}", style_body)],
        [Paragraph("QA Automation & Security Audits", style_body), Paragraph("Automated regression suites, vulnerability scanning, penetration prep", style_body), Paragraph(f"{format_inr(costs.get('qa_testing_cost', 0.0))}", style_body)],
        [Paragraph("DevOps, Cloud Architecture & CI/CD", style_body), Paragraph("Infrastructure-as-Code (Terraform), Docker/Kubernetes staging clusters", style_body), Paragraph(f"{format_inr(costs.get('devops_cloud_cost', 0.0))}", style_body)],
        [Paragraph("Agile Governance & Project Management", style_body), Paragraph("Sprint ceremonies, weekly executive reporting, milestone sign-offs", style_body), Paragraph(f"{format_inr(costs.get('project_management_cost', 0.0))}", style_body)],
        [Paragraph("Principal Solution Architecture", style_body), Paragraph("System blueprint, entity schemas, non-functional requirements oversight", style_body), Paragraph(f"{format_inr(costs.get('architecture_cost', 0.0))}", style_body)],
    ]

    if costs.get("compliance_cost", 0.0) > 0:
        financial_rows.append([
            Paragraph("Regulatory Compliance Specialist", style_body),
            Paragraph(f"Industry regulatory alignment for {profile.get('compliance_standards', ['Compliance'])[0]}", style_body),
            Paragraph(f"{format_inr(costs.get('compliance_cost', 0.0))}", style_body)
        ])

    financial_rows.append([
        Paragraph("Staging Cloud Infra & Tooling", style_body),
        Paragraph(f"Cloud test environment, database instances, and sandbox licenses during implementation", style_body),
        Paragraph(f"{format_inr(costs.get('infrastructure_staging_cost', 0.0))}", style_body)
    ])

    financial_rows.append([
        Paragraph("<b>Engineering Subtotal</b>", style_body_bold),
        Paragraph("Base effort across all 7 development phases", style_body),
        Paragraph(f"<b>{format_inr(subtotal)}</b>", style_body_bold)
    ])

    financial_rows.append([
        Paragraph(f"Contingency Reserve ({contingency_pct}%)", style_body),
        Paragraph("Risk buffer for unforeseen integration complexities & scope changes", style_body),
        Paragraph(f"{format_inr(contingency)}", style_body)
    ])

    if discount > 0:
        financial_rows.append([
            Paragraph("Commercial Partnership Discount", style_body),
            Paragraph("Special initiative courtesy concession", style_body),
            Paragraph(f"-{format_inr(discount)}", style_body)
        ])

    financial_rows.append([
        Paragraph(f"Applicable GST / Taxes ({tax_pct}%)", style_body),
        Paragraph("Standard commercial service tax assessment (18% GST)", style_body),
        Paragraph(f"{format_inr(tax)}", style_body)
    ])

    financial_rows.append([
        Paragraph("<b>TOTAL PROJECT INVESTMENT</b>", style_h3),
        Paragraph(f"<b>Fixed-fee delivery guarantee backed by Quotflow SLA</b>", style_body_bold),
        Paragraph(f"<b><font size=11 color='{primary_hex}'>{format_inr(grand_total)} INR</font></b>", style_body_bold)
    ])

    t_fin = Table(financial_rows, colWidths=[page_width * 0.35, page_width * 0.45, page_width * 0.20])
    t_fin.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("PADDING", (0, 0), (-1, -1), 4.5),
        ("ALIGN", (2, 0), (2, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, -2), (-1, -2), 1, c_primary),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor(profile.get("bg_soft", "#eff6ff"))),
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 10))

    # 10. PAYMENT MILESTONES
    story.append(Paragraph("8. Payment Milestones Schedule", style_h2))
    milestones = estimation_data.get("payment_milestones", [])
    m_rows = [
        [
            Paragraph("<b>Milestone Name</b>", style_body_bold),
            Paragraph("<b>Deliverable Trigger / Sign-Off Criteria</b>", style_body_bold),
            Paragraph("<b>Split</b>", style_body_bold),
            Paragraph("<b>Amount (INR)</b>", style_body_bold)
        ]
    ]
    for m in milestones:
        m_rows.append([
            Paragraph(f"<b>{m.get('milestone')}</b>", style_body),
            Paragraph(m.get("trigger", "Milestone acceptance criteria fulfilled."), style_body),
            Paragraph(f"{m.get('percentage')}%", style_body),
            Paragraph(f"<b>{format_inr(m.get('amount', 0.0))}</b>", style_body_bold)
        ])
    t_m = Table(m_rows, colWidths=[page_width * 0.32, page_width * 0.46, page_width * 0.08, page_width * 0.14])
    t_m.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_light])
    ]))
    story.append(t_m)
    story.append(Spacer(1, 12))

    # 11. ASSUMPTIONS, EXCLUSIONS, WARRANTY & SIGNATURE BLOCK
    terms_block = []
    terms_block.append(Paragraph("9. Engagement Terms, Warranty & Acceptance", style_h2))
    terms_text = (
        f"<b>1. Intellectual Property Transfer:</b> 100% of custom source code, documentation, and design assets "
        f"will be transferred to {cust.get('company', 'Client')} upon settlement of the final milestone payment.<br/>"
        f"<b>2. 90-Day Hypercare Warranty:</b> Quotflow provides 90 days of priority defect rectification post-launch "
        f"at zero additional cost, backed by our {profile.get('sla_terms', '99.9% uptime SLA')}.<br/>"
        f"<b>3. Exclusions:</b> Third-party SaaS subscription fees (e.g. AWS hosting, Epic API licensing, Stripe fees) "
        f"are direct vendor expenses and not included in this engineering services quotation.<br/>"
        f"<b>4. Change Management:</b> Material changes in project scope will be formally evaluated via mutual Change Request (CR) "
        f"at standard consulting billing rates."
    )
    terms_block.append(Paragraph(terms_text, style_small))
    terms_block.append(Spacer(1, 14))

    # Dual Signature Table - Featuring Developer & Authorized Signatory: Kaitha Bhanuteja
    sig_data = [
        [
            Paragraph(f"<b>ACCEPTED AND AGREED:</b><br/>"
                      f"<b>For {cust.get('company', 'Client Organization')}:</b><br/><br/><br/>"
                      f"__________________________________________<br/>"
                      f"Authorized Signature<br/><br/>"
                      f"Name: {cust.get('name', 'Client Representative')}<br/>"
                      f"Title: {cust.get('designation', 'Authorized Signatory')}<br/>"
                      f"Date: ________________________", style_body),
            Paragraph(f"<b>ISSUED BY:</b><br/>"
                      f"<b>For Quotflow Technologies Limited:</b><br/><br/><br/>"
                      f"__________________________________________<br/>"
                      f"Authorized Signature<br/><br/>"
                      f"Name: Kaitha Bhanuteja<br/>"
                      f"Title: Authorized Signatory & Solutions Delivery Head<br/>"
                      f"Date: {datetime.now().strftime('%B %d, %Y')}", style_body)
        ]
    ]
    t_sig = Table(sig_data, colWidths=[page_width * 0.5, page_width * 0.5])
    t_sig.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("BACKGROUND", (0, 0), (-1, -1), c_light),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    terms_block.append(t_sig)

    story.append(KeepTogether(terms_block))

    # Pass quotation ref to NumberedCanvas for running headers
    def canvas_factory(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c.ref_no = quotation_ref
        return c

    doc.build(story, canvasmaker=canvas_factory)
    logger.info(f"Generated PDF Quotation successfully at {output_path}")
    return str(output_path)

# Quotflow.ai - AI-Powered Quotation Management System

A production-grade, enterprise-ready **AI-Powered Quotation Management Platform** developed by **Kaitha Bhanuteja** for **Quotflow Technologies Limited**.

Built with **Python, Flask, MySQL, SQLAlchemy, Google Gemini API, Pydantic, and ReportLab**.

---

## 🏢 Corporate & Developer Information

- **Product Name**: Quotflow.ai
- **Organization**: Quotflow Technologies Limited
- **Location**: Madhapur, HITEC City, Hyderabad, Telangana, India
- **Lead Developer**: **Kaitha Bhanuteja**
- **Default Currency**: Indian Rupee (`₹ INR`) with Indian comma grouping (e.g. `₹1,50,000`, `₹12,50,000`)
- **Authorized Signatory**: **Kaitha Bhanuteja**

---

## 🚀 Key Highlights & Architecture

```
                        [Customer Inquiry Email Intake]
                                      │
                                      ▼
                        [Google Gemini API Engine]
             (Structured Pydantic Extraction + Intelligent Heuristic Fallback)
             ┌────────────────────────┴────────────────────────┐
             ▼                                                 ▼
[Autonomous Industry Detection]                 [Requirement & Complexity Engine]
 - Healthcare, FinTech, Logistics,               - Confirmed vs AI Assumptions
   E-Commerce, EdTech, PropTech, etc.            - Missing Info Clarification Questions
 - Custom / Unknown Industry Synthesis           - Complexity Scoring (1-100)
             │                                                 │
             └────────────────────────┬────────────────────────┘
                                      ▼
                 [Deterministic Python Estimation Engine]
                   - Effort: Hours across 7 Project Phases
                   - Team Allocation: Roles, Seniority, Headcount, Rates (₹)
                   - Itemized Financials: Dev, Integrations, QA, DevOps, Staging
                   - Risk Contingency (10%), 18% GST / Taxes, Milestones (25% x 4)
                   - Methodology & Calculation Transparency (₹)
                                      │
                                      ▼
                 [MySQL / SQLAlchemy Quotation Management]
                   - Customer & Project Master Records
                   - Immutable Version Tracking (v1, v2, v3...)
                   - Status Pipeline (Draft ➔ In Review ➔ Approved ➔ Sent)
                   - Audit Trail & Activity Log
                                      │
                                      ▼
                   [ReportLab Platypus PDF Generator]
                   - Multi-Page Document with NumberedCanvas ("Page X of Y")
                   - Dynamic Industry Visual Accents & Compliance Matrix
                   - Letterhead, Indian Rupee Ledger (₹), Sign-off Blocks
                   - Authorized Signatory: Kaitha Bhanuteja
```

---

## 🛠️ Features Breakdown

### 1. Modern SaaS UI Redesign
- Designed like modern B2B SaaS software (Linear, Stripe, Retool).
- Spacious cards with visual hierarchy, subtle hairline borders (`#e2e8f0`), and soft shadows.
- Distinct color coding for Confirmed requirements (Forest Green) and AI Inferred Assumptions (Amber).
- Horizontal SaaS stepper pipeline with step badges and active progress rings.
- Refined typography (Inter & Plus Jakarta Sans) and comfortable, generous padding throughout.
- Fully responsive across desktop, tablet, and mobile displays.

### 2. Indian Currency Formatting (`₹ INR`)
- Complete adoption of the Indian numbering system throughout UI, tables, KPI metric cards, and generated PDFs.
- Indian comma grouping:
  - Example: `₹1,50,000`
  - Example: `₹12,50,000`
- Applied consistently to resource hourly rates, development costs, integrations, QA, DevOps, cloud staging, contingency reserve, 18% GST / taxes, discounts, and payment milestones.

### 3. Developer & Signatory Attribution
- **Kaitha Bhanuteja** is attributed in:
  - System footer & letterhead profile
  - System settings and diagnostics overview
  - Official Quotation PDF **Authorized Signatory** block

### 4. Automatic Industry Detection (100% Autonomous)
- **Zero manual dropdowns or selection required.** The system detects the domain directly from vocabulary, regulatory standards, and integration specs.
- Archetypes:
  - **Healthcare & MedTech** (HIPAA, HITECH, HL7/FHIR, EHR/EMR, PHI encryption)
  - **FinTech & Banking** (PCI-DSS Level 1, SOC-2, double-entry ledger, KYC/AML)
  - **Logistics & Supply Chain** (IoT telematics, GPS geofencing, route dispatch, FMCSA ELD)
  - **E-Commerce & Retail** (Omnichannel cart, Elasticsearch catalog, multi-currency)
  - **EdTech & E-Learning** (SCORM 2004, xAPI, LTI 1.3, FERPA)
  - **Real Estate & PropTech** (RESO Web API, MLS/IDX sync, 3D tour viewer)
  - **Manufacturing & Industrial IoT** (OPC-UA, MQTT, OEE dashboards)
  - **Custom / Unknown Industries** (e.g. Precision AgTech Drones, BioTech): Dynamically synthesizes custom deliverables, compliance standards, and phase roadmaps!

### 5. Deterministic Python Cost Calculation Engine
- Standard hourly rate card by seniority.
- Accounts for **team concurrency** (e.g., 2.6 parallel velocity) to calculate calendar weeks and working days.
- Structured **4-Tranche Milestone Schedule** (Mobilization 25%, Alpha 25%, Beta 25%, Final UAT 25%).
- Configurable **Risk Contingency (10%)** and **18% GST / Taxes**.
- Interactive **Estimation Editor**: Users can adjust hours, rates, contingency %, and taxes in real-time before generating the final quote.

### 6. Executive ReportLab PDF Quotation
- Custom `NumberedCanvas` prints **"Page X of Y"**, quotation reference, and confidentiality footer.
- Embedded TrueType fonts for clear Indian Rupee (`₹`) rendering.
- Official Letterhead: Quotflow Technologies Limited, Madhapur, HITEC City, Hyderabad.
- Scope of Work Matrix (Confirmed vs Inferred).
- Implementation Phases & Roadmap Table.
- Resource Allocation & Staff Plan.
- Itemized Financial Summary Ledger in `₹ INR`.
- Payment Milestones Schedule.
- 90-Day Hypercare Warranty, SLA Terms, and Exclusions.
- Formal Sign-off and Acceptance Block with **Kaitha Bhanuteja**.

---

## ⚡ Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Key parameters:
- `GEMINI_API_KEY`: Google Gemini API key (optional; built-in NLP engine runs if blank).
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`: (optional; falls back automatically to SQLite `quoteflow.db`).
- `COMPANY_NAME=Quotflow Technologies Limited`
- `COMPANY_ADDRESS=Madhapur, HITEC City, Hyderabad, Telangana, India`
- `DEVELOPER_NAME=Kaitha Bhanuteja`
- `DEFAULT_CURRENCY=INR`

### 3. Run Test Suite
```bash
python -m unittest tests/test_services.py
```
*Expected: 11/11 tests pass.*

### 4. Start the Application
```bash
python app.py
```
Open your browser to:
👉 **`http://localhost:5000`**

---

## 📄 Creator & License
Designed & Developed by **Kaitha Bhanuteja** for **Quotflow Technologies Limited** (Hyderabad, Telangana, India).

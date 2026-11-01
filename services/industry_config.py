"""
Industry-Specific Archetypes and Dynamic Configuration Engine.
Provides distinct deliverables, compliance frameworks, implementation phases,
terminology, and visual branding palettes for each industry.
"""

INDUSTRY_PROFILES = {
    "Healthcare & MedTech": {
        "code": "MED",
        "badge_color": "#0d9488",  # Teal
        "accent_color": "#115e59",
        "bg_soft": "#f0fdfa",
        "compliance_standards": [
            "HIPAA (Health Insurance Portability and Accountability Act)",
            "HITECH Act & Omnibus Rule",
            "HL7 v2/v3 and FHIR (Fast Healthcare Interoperability Resources)",
            "FDA 21 CFR Part 11 (Audit trails & Electronic signatures)",
            "SOC-2 Type II Healthcare Trust Services"
        ],
        "key_deliverables": [
            "Encrypted PHI (Protected Health Information) Storage Architecture",
            "FHIR/HL7 Compliant Interoperability & EHR/EMR Integration Layer",
            "Telehealth WebRTC Encrypted Video Consultation Engine",
            "Clinical Decision Support & Prescription Workflow Module",
            "Role-Based Access Control (Clinician, Patient, Admin, Auditor)",
            "Immutable Medical Audit Trail & Compliance Reporting Engine"
        ],
        "terminology": {
            "user_entity": "Patient / Clinician",
            "transaction_entity": "Clinical Encounter / Appointment",
            "data_record": "Electronic Health Record (EHR / PHI)",
            "primary_audit": "HIPAA Privacy & Security Audit",
            "operational_metric": "Patient Care Turnaround Time & Encrypted Throughput"
        },
        "standard_phases": [
            {"phase": "Phase 1: HIPAA Compliance & Architecture Discovery", "weeks": 2, "description": "Security protocols, BAA alignment, EHR data mapping, FHIR schemas."},
            {"phase": "Phase 2: UI/UX & Accessible Clinical Workflows", "weeks": 3, "description": "Patient portal, Doctor dashboard, WCAG 2.1 AA accessibility design."},
            {"phase": "Phase 3: Core Medical Engine & Encryption Vault", "weeks": 6, "description": "AES-256 encrypted PHI repository, patient scheduling, video consultation."},
            {"phase": "Phase 4: EHR/EMR & Diagnostic Integrations", "weeks": 4, "description": "Integration with Epic/Cerner/AthenaHealth APIs, Lab HL7 feeds."},
            {"phase": "Phase 5: HIPAA Security Audit & Pen-Testing", "weeks": 3, "description": "Vulnerability scanning, third-party HIPAA pen-test, failover drills."},
            {"phase": "Phase 6: Deployment, BAA Signing & Clinical Training", "weeks": 2, "description": "HIPAA-compliant AWS/GCP setup, staff training, Go-Live hypercare."}
        ],
        "sla_terms": "99.99% high-availability SLA with 24/7 BAA-covered emergency support, 15-minute response for P1 patient-care incidents."
    },
    
    "FinTech & Banking": {
        "code": "FIN",
        "badge_color": "#1e3a8a",  # Deep Navy
        "accent_color": "#b45309",  # Gold / Amber
        "bg_soft": "#eff6ff",
        "compliance_standards": [
            "PCI-DSS v4.0 Level 1 Certification Standards",
            "SOC-2 Type II (Security, Availability, Confidentiality)",
            "FinCEN Anti-Money Laundering (AML) & KYC Rules",
            "GDPR / GLBA (Gramm-Leach-Bliley Act) Financial Privacy",
            "PSD2 / Open Banking Regulatory Frameworks"
        ],
        "key_deliverables": [
            "Zero-Trust Multi-Tier Financial Architecture",
            "Immutable Double-Entry General Ledger Engine",
            "PCI-DSS Tokenized Payment & Card Vault Gateway",
            "Real-time KYC/AML Verification & Identity Proofing Pipeline",
            "AI-Powered Fraud Anomaly Detection & Velocity Rules Engine",
            "Multi-Currency Settlement & Bank Reconciliation Middleware"
        ],
        "terminology": {
            "user_entity": "Account Holder / Merchant",
            "transaction_entity": "Financial Ledger Transaction",
            "data_record": "Cardholder Data (CHD) / Audit Log",
            "primary_audit": "PCI-DSS Level 1 & SOC-2 Audit",
            "operational_metric": "Transaction TPS & Sub-second Settlement Latency"
        },
        "standard_phases": [
            {"phase": "Phase 1: FinTech Architecture & Regulatory Mapping", "weeks": 2, "description": "Banking API specifications, PCI boundary definition, ledger schema."},
            {"phase": "Phase 2: High-Trust UI/UX & Onboarding Flows", "weeks": 3, "description": "Frictionless KYC/AML UI, mobile biometric auth, transaction views."},
            {"phase": "Phase 3: Ledger Engine & Payment Rails Core", "weeks": 7, "description": "Double-entry ledger, multi-currency routing, webhook reconciliation."},
            {"phase": "Phase 4: Banking APIs & Payment Gateway Integrations", "weeks": 4, "description": "Stripe/Plaid/ACH rails, biometric KYC provider, anti-fraud rules."},
            {"phase": "Phase 5: Financial Stress Testing & Security Penetration", "weeks": 3, "description": "Red-team penetration testing, ledger balance stress testing, PCI audit prep."},
            {"phase": "Phase 6: Production Hardening & Disaster Recovery Launch", "weeks": 2, "description": "Multi-region active-active deployment, automated audit logging, Go-Live."}
        ],
        "sla_terms": "99.999% financial uptime guarantee, sub-50ms transaction API latency, dedicated financial security response team."
    },

    "Logistics & Supply Chain": {
        "code": "LOG",
        "badge_color": "#047857",  # Emerald
        "accent_color": "#065f46",
        "bg_soft": "#ecfdf5",
        "compliance_standards": [
            "DOT / FMCSA Electronic Logging Device (ELD) Mandates",
            "ISO 28000 Security Management for Supply Chains",
            "HAZMAT Transportation Compliance Standards",
            "GS1 Global Standards for Barcoding & EPCIS Tracking"
        ],
        "key_deliverables": [
            "Real-Time IoT Telematics & GPS Fleet Tracking Gateway",
            "Dynamic AI Route Optimization & Geofencing Engine",
            "Cross-Platform Driver & Dispatch Mobile Applications",
            "Multi-Warehouse Inventory & Barcode/RFID Sync Engine",
            "Automated Bill of Lading (BoL) & Proof of Delivery (PoD)",
            "Carrier Rate Calculation & Freight Audit Reconciliation"
        ],
        "terminology": {
            "user_entity": "Dispatcher / Fleet Driver / Shipper",
            "transaction_entity": "Consignment / Shipment Order",
            "data_record": "Proof of Delivery (PoD) / Telematics Log",
            "primary_audit": "ELD & Supply Chain Tracking Audit",
            "operational_metric": "On-Time In-Full (OTIF) Delivery & Fleet Fuel Efficiency"
        },
        "standard_phases": [
            {"phase": "Phase 1: Fleet Logistics Discovery & Field Mapping", "weeks": 2, "description": "Hardware IoT specs, carrier API mapping, route logic design."},
            {"phase": "Phase 2: Dispatcher Dashboard & Driver UX", "weeks": 3, "description": "Interactive map cockpit, offline-capable driver mobile app flow."},
            {"phase": "Phase 3: Core Telematics & Route Optimization Engine", "weeks": 6, "description": "Real-time websocket telematics, ETA recalculation, geofence alerts."},
            {"phase": "Phase 4: Warehouse (WMS) & Carrier Integrations", "weeks": 4, "description": "Integration with TMS, ERP (SAP), FedEx/UPS/freight APIs, PoD capture."},
            {"phase": "Phase 5: High-Concurrency Stress & Field Simulation", "weeks": 3, "description": "Simulated 10,000 active vehicle telemetry pings, offline sync tests."},
            {"phase": "Phase 6: Multi-Hub Staging & Fleet Rollout", "weeks": 2, "description": "Driver app store release, dispatcher team training, 24/7 Go-Live monitoring."}
        ],
        "sla_terms": "99.95% cloud availability with offline driver app fallback mode, 30-minute SLA for dispatch-blocking incidents."
    },

    "E-Commerce & Omnichannel Retail": {
        "code": "ECM",
        "badge_color": "#7c3aed",  # Violet
        "accent_color": "#5b21b6",
        "bg_soft": "#f5f3ff",
        "compliance_standards": [
            "PCI-DSS Level 2/3 Compliance for Checkout Rails",
            "GDPR / CCPA Consumer Privacy and Cookie Consent",
            "ADA Title III / WCAG 2.1 AA E-Commerce Accessibility"
        ],
        "key_deliverables": [
            "Headless High-Speed Product Catalog & Elasticsearch Storefront",
            "Omnichannel Cart, Multi-Currency & Localized Checkout Pipeline",
            "Real-time Inventory Allocation & Warehouse Management Sync",
            "Customer Loyalty, Discount Engine & Cart Abandonment Flow",
            "Merchant Vendor Portal with Commission & Payout Automation",
            "High-Throughput CDN & Edge Caching Architecture (Sub-second FCP)"
        ],
        "terminology": {
            "user_entity": "Shopper / Merchant Vendor",
            "transaction_entity": "Order / Cart Checkout",
            "data_record": "SKU Inventory Item / Order Receipt",
            "primary_audit": "Conversion Rate & Load Spike Audit",
            "operational_metric": "Cart Conversion Rate, Average Order Value & Page Load Time"
        },
        "standard_phases": [
            {"phase": "Phase 1: Catalog Architecture & UX Journey Mapping", "weeks": 2, "description": "Information architecture, category taxonomy, checkout wireframes."},
            {"phase": "Phase 2: High-Converting Storefront & Responsive Design", "weeks": 3, "description": "Mobile-first store UI, fast filter navigation, micro-interactions."},
            {"phase": "Phase 3: Core Commerce Engine & Order Management", "weeks": 6, "description": "Cart engine, tax calculations, dynamic promotions, customer portal."},
            {"phase": "Phase 4: Payment Rails, ERP & WMS Integrations", "weeks": 4, "description": "Stripe/PayPal, Shopify/Shopify Plus/ERP sync, shipping carriers."},
            {"phase": "Phase 5: Flash-Sale Load Testing & Security Audit", "weeks": 3, "description": "Black Friday load simulation (50k concurrent carts), CDN optimization."},
            {"phase": "Phase 6: Global Edge CDN Deployment & Storefront Launch", "weeks": 2, "description": "DNS cutover, Google Analytics 4 tracking, 30-day post-launch support."}
        ],
        "sla_terms": "99.95% uptime during peak holiday traffic, 90th percentile response time under 300ms globally."
    },

    "EdTech & E-Learning": {
        "code": "EDT",
        "badge_color": "#d97706",  # Amber
        "accent_color": "#b45309",
        "bg_soft": "#fffbeb",
        "compliance_standards": [
            "FERPA (Family Educational Rights and Privacy Act)",
            "COPPA (Children's Online Privacy Protection Act)",
            "SCORM 1.2 / SCORM 2004 & xAPI (Experience API) Standards",
            "LTI 1.3 (Learning Tools Interoperability) Certification"
        ],
        "key_deliverables": [
            "Adaptive Learning Curriculum & Modular Course Player",
            "SCORM/xAPI Compliant Course Content Consumption Engine",
            "Real-time Interactive Quiz, Grading & Assessment Module",
            "Low-Latency Adaptive Bitrate Video Streaming with DRM",
            "Student Progress Analytics, Badges & Certification Generation",
            "Institutional LMS Sync (Canvas, Blackboard, Moodle) via LTI"
        ],
        "terminology": {
            "user_entity": "Student / Instructor / Academic Admin",
            "transaction_entity": "Course Enrollment / Assessment Submission",
            "data_record": "Learner Progress Record / Gradebook",
            "primary_audit": "FERPA Compliance & Content Delivery Audit",
            "operational_metric": "Course Completion Rate & Student Engagement Score"
        },
        "standard_phases": [
            {"phase": "Phase 1: Pedagogical Architecture & Curriculum Mapping", "weeks": 2, "description": "LMS interoperability specs, student role matrix, SCORM mapping."},
            {"phase": "Phase 2: Accessible Learner & Instructor Experience", "weeks": 3, "description": "Distraction-free course player, quiz UI, grading workbench."},
            {"phase": "Phase 3: Core Learning Management System (LMS)", "weeks": 5, "description": "Course authoring, video player integration, automated certificate generation."},
            {"phase": "Phase 4: Institutional LTI & Third-Party Integrations", "weeks": 4, "description": "Canvas/Moodle LTI 1.3 connectors, Zoom/Google Meet classroom APIs."},
            {"phase": "Phase 5: Multi-Device Testing & FERPA Verification", "weeks": 3, "description": "Cross-device browser testing, accessibility (WCAG 2.1), load testing."},
            {"phase": "Phase 6: Semester Handover, Deployment & Admin Onboarding", "weeks": 2, "description": "Cloud hosting rollout, faculty training sessions, semester launch."}
        ],
        "sla_terms": "99.9% uptime with zero buffering video CDN guarantee, dedicated exam-day support hotline."
    },

    "Real Estate & PropTech": {
        "code": "PRP",
        "badge_color": "#0284c7",  # Sky Blue
        "accent_color": "#0369a1",
        "bg_soft": "#f0f9ff",
        "compliance_standards": [
            "RESO (Real Estate Standards Organization) Web API Standards",
            "Fair Housing Act Digital Accessibility & Non-Discrimination",
            "ESIGN Act & UETA for Binding Digital Leases"
        ],
        "key_deliverables": [
            "Automated MLS / IDX Real Estate Listing Feed Aggregator",
            "Interactive Map-Based Property Search & Neighborhood Analytics",
            "Virtual 3D Tour & High-Definition Media Streaming Pipeline",
            "Tenant Portal with Online Rent Collection & Lease Signatures",
            "Automated Maintenance Ticket Dispatching & Contractor Bidding",
            "Investor Cap Rate & Cash-on-Cash Return Yield Calculator"
        ],
        "terminology": {
            "user_entity": "Buyer / Tenant / Broker / Property Manager",
            "transaction_entity": "Property Inquiry / Lease Agreement",
            "data_record": "MLS Listing / Tenant Ledger",
            "primary_audit": "RESO Compliance & Fair Housing Audit",
            "operational_metric": "Listing Inquiries, Days on Market & Lead-to-Tour Ratio"
        },
        "standard_phases": [
            {"phase": "Phase 1: MLS Feed Discovery & Schema Mapping", "weeks": 2, "description": "RESO Web API credentials, listing normalization, search taxonomy."},
            {"phase": "Phase 2: Immersive Property Browsing UI/UX", "weeks": 3, "description": "Map-centric UI, 3D tour viewers, tenant application workflows."},
            {"phase": "Phase 3: Property Portal & Real-time Sync Engine", "weeks": 6, "description": "IDX crawler, automated email alerts, tenant lease management."},
            {"phase": "Phase 4: DocuSign, Stripe & Screening Integrations", "weeks": 4, "description": "Tenant credit screening APIs, DocuSign e-sign, payment gateway."},
            {"phase": "Phase 5: Performance Tuning & Geocoding Verification", "weeks": 3, "description": "Map clustering load tests, MLS sync reliability checks."},
            {"phase": "Phase 6: Brokerage Launch & Agent Training", "weeks": 2, "description": "Domain launch, SEO indexing setup, agent dashboard training."}
        ],
        "sla_terms": "99.9% uptime, 15-minute MLS data refresh synchronization guarantee."
    },

    "Manufacturing & Industrial IoT": {
        "code": "MFG",
        "badge_color": "#475569",  # Slate
        "accent_color": "#334155",
        "bg_soft": "#f8fafc",
        "compliance_standards": [
            "ISA-95 Enterprise-Control System Integration Standard",
            "OPC-UA (Open Platform Communications Unified Architecture)",
            "ISO 9001 Quality Management & Traceability Requirements",
            "IEC 62443 Industrial Network & System Security"
        ],
        "key_deliverables": [
            "High-Throughput MQTT / OPC-UA Industrial Telemetry Broker",
            "Overall Equipment Effectiveness (OEE) Real-Time Dashboard",
            "Machine Learning Predictive Maintenance Anomaly Detector",
            "Digital Twin Machine Hierarchy & Component Health Tracking",
            "Shop-Floor Operator Touchscreen Terminal Interface",
            "Batch Traceability, Bill of Materials (BOM) & ERP Bridge"
        ],
        "terminology": {
            "user_entity": "Plant Manager / Machine Operator / Reliability Engineer",
            "transaction_entity": "Production Work Order / Maintenance Event",
            "data_record": "Telemetry Time-Series / Quality Inspection Record",
            "primary_audit": "ISA-95 & Plant Floor Security Audit",
            "operational_metric": "Overall Equipment Effectiveness (OEE) & Mean Time Between Failures (MTBF)"
        },
        "standard_phases": [
            {"phase": "Phase 1: PLC/SCADA & Factory Network Discovery", "weeks": 2, "description": "Protocol audit (Modbus/OPC-UA), edge hardware specs, data cadence."},
            {"phase": "Phase 2: Industrial Dashboard & Operator UX", "weeks": 3, "description": "High-contrast shop floor UI, executive KPI charts, mobile alerts."},
            {"phase": "Phase 3: High-Frequency Telemetry Ingestion Engine", "weeks": 6, "description": "Time-series database, real-time alert trigger, OEE calculation."},
            {"phase": "Phase 4: ERP/MES & Sensor Gateway Integration", "weeks": 4, "description": "SAP/Oracle MES bridge, edge gateway firmware connectors."},
            {"phase": "Phase 5: Factory Floor Simulation & Edge Failover", "weeks": 3, "description": "Simulated plant line stress test, offline buffer recovery."},
            {"phase": "Phase 6: Plant Deployment & Reliability Onboarding", "weeks": 2, "description": "Edge gateway installation, plant manager training, Go-Live."}
        ],
        "sla_terms": "99.95% plant floor uptime, sub-second telemetry alert dispatch guarantee."
    }
}


def get_industry_profile(industry_name: str) -> dict:
    """
    Retrieves the industry profile for a given industry name.
    If the industry is unknown or custom, dynamically synthesizes a tailored profile
    so that every single industry gets unique, domain-specific quotation content!
    """
    # Direct match or case-insensitive match
    for name, profile in INDUSTRY_PROFILES.items():
        if name.lower() in industry_name.lower() or industry_name.lower() in name.lower():
            res = profile.copy()
            res["industry_name"] = name
            return res

    # Unknown / Custom Industry: Dynamically generate a tailored profile!
    cleaned_name = industry_name.strip() if industry_name else "Enterprise Custom Solutions"
    words = [w.capitalize() for w in cleaned_name.split() if w.isalnum()]
    code = "".join([w[:2].upper() for w in words[:2]]) or "CUS"
    
    return {
        "industry_name": cleaned_name,
        "code": code,
        "badge_color": "#2563eb",  # Modern Royal Blue
        "accent_color": "#1d4ed8",
        "bg_soft": "#eff6ff",
        "compliance_standards": [
            f"Industry Standard Compliance for {cleaned_name}",
            "SOC-2 Type II Security & Data Integrity Baseline",
            "ISO/IEC 27001 Information Security Management",
            "GDPR / Regional Data Protection Regulations"
        ],
        "key_deliverables": [
            f"Custom High-Availability Architecture Tailored for {cleaned_name}",
            f"Domain-Specific Workflow Engine for {cleaned_name} Operations",
            "Enterprise Role-Based Access Control & Identity Management",
            "Comprehensive Third-Party API Integration & Data Pipeline",
            "Interactive Reporting, Analytics & Executive KPI Dashboard",
            "Automated Audit Logging & System Health Telemetry"
        ],
        "terminology": {
            "user_entity": f"{cleaned_name} Stakeholder / End User",
            "transaction_entity": f"{cleaned_name} Operational Event",
            "data_record": f"{cleaned_name} Domain Record",
            "primary_audit": f"{cleaned_name} Operational Security Review",
            "operational_metric": "Operational Throughput & Workflow Efficiency"
        },
        "standard_phases": [
            {"phase": f"Phase 1: {cleaned_name} Requirements & Solution Architecture", "weeks": 2, "description": "Domain analysis, architecture blueprint, API specification."},
            {"phase": "Phase 2: Interactive Wireframing & Design System", "weeks": 3, "description": "User journeys, role permissions, responsive interface design."},
            {"phase": f"Phase 3: Core {cleaned_name} Functional Engine", "weeks": 6, "description": "Core workflows, data modeling, backend business logic."},
            {"phase": "Phase 4: API Integrations & External Data Connectors", "weeks": 4, "description": "Third-party APIs, legacy system bridge, automated sync."},
            {"phase": "Phase 5: Comprehensive QA, Security & Performance Hardening", "weeks": 3, "description": "End-to-end testing, security scanning, user acceptance testing."},
            {"phase": "Phase 6: Cloud Production Deployment & Handover", "weeks": 2, "description": "CI/CD pipeline, production launch, admin team training & hypercare."}
        ],
        "sla_terms": "99.9% uptime SLA with 24/7 technical monitoring, dedicated engineering support."
    }

"""
Realistic customer inquiry emails representing different industries and complexities.
Each email has clear business context, functional requirements, technical notes,
and natural ambiguities that test the AI's extraction and clarification questioning.
"""

SAMPLE_EMAILS = [
    {
        "id": "healthcare_ehr",
        "title": "Healthcare: Telehealth & Patient EHR Portal",
        "industry_hint": "Healthcare & MedTech",
        "subject": "Request for Quotation: Enterprise Telehealth & Patient EHR Integration Platform",
        "sender_name": "Dr. Sarah Jenkins",
        "sender_email": "sjenkins@apexhealthgroup.org",
        "sender_company": "Apex Health Group",
        "sender_phone": "+1 (555) 234-8901",
        "body": """Dear QuoteFlow Team,

I am writing on behalf of Apex Health Group. We operate a network of 14 outpatient clinics across the Pacific Northwest and are seeking an engineering partner to develop a centralized Telehealth and Patient Care Portal.

Our primary business objective is to expand remote consultations while giving patients direct digital access to their clinical records, lab test results, and billing statements.

Key Functional Requirements:
1. Patient portal: Web and mobile responsive interface for booking video appointments, completing intake forms, and viewing medical history.
2. Provider clinical workbench: Doctor dashboard with patient queue, e-prescription generation, and clinical notes charting.
3. High-definition WebRTC video consultation with end-to-end encryption and virtual waiting rooms.
4. Secure two-way messaging between doctors and patients with attachment support for diagnostic scans.
5. Online copay and invoice payments.

Technical & Integration Needs:
- Must integrate seamlessly with our existing Epic Systems EHR via FHIR / HL7 APIs to synchronize patient records in real time.
- All stored and in-transit data must strictly comply with HIPAA and HITECH regulations (AES-256 encryption, role-based access, comprehensive audit trails).
- We plan to host this on AWS (GovCloud or HIPAA-compliant VPC).
- Expected load: Approximately 45,000 active patients and 120 attending physicians.

We would like to launch an initial beta within 4 to 5 months. Could you please provide a formal quotation detailing implementation phases, team composition, resource costs, and project milestones?

Sincerely,
Dr. Sarah Jenkins, MD, Chief Medical Information Officer
Apex Health Group
sjenkins@apexhealthgroup.org
(555) 234-8901"""
    },
    {
        "id": "fintech_banking",
        "title": "FinTech: Multi-Currency Digital Banking App",
        "industry_hint": "FinTech & Banking",
        "subject": "RFP: Multi-Currency Neo-Banking Platform with Real-time Ledger & PCI Compliance",
        "sender_name": "Marcus Vance",
        "sender_email": "m.vance@apexcapitalpartners.io",
        "sender_company": "Apex Capital Partners",
        "sender_phone": "+1 (212) 555-7822",
        "body": """Hello QuoteFlow Team,

Apex Capital is launching a cross-border digital financial platform tailored for digital nomads and global SMEs. We are requesting a comprehensive quotation and technical proposal for developing the MVP and v1 production system.

Scope & Core Features:
- Multi-currency digital wallet supporting USD, EUR, GBP, and SGD with automated exchange rate conversion.
- Double-entry transaction ledger engine ensuring mathematical reconciliation and zero-balance integrity.
- Automated KYC/AML onboarding workflow with automated identity verification, passport OCR, and sanctions list screening.
- Virtual and physical debit card issuance with instant freeze/unfreeze and spending limits.
- Real-time push notifications, monthly statements (PDF export), and recurring payroll scheduled payments.

Technical Requirements & Constraints:
- Architecture must meet PCI-DSS Level 1 compliance guidelines, with cardholder data tokenized and isolated in a dedicated vault.
- Integration with Plaid for bank account linking and Stripe Issuing / Marqeta for card rails.
- High-frequency event processing with sub-100ms API response times.
- Zero-trust authentication with biometric FaceID/TouchID and TOTP multi-factor authentication.

Could your team provide an itemized cost estimate, expected timeline, resource allocation, and payment schedule? We have board approval and wish to start in Q1.

Best regards,
Marcus Vance, Head of Product & Technology
Apex Capital Partners
m.vance@apexcapitalpartners.io"""
    },
    {
        "id": "logistics_fleet",
        "title": "Logistics: AI Fleet Telematics & Route Dispatch",
        "industry_hint": "Logistics & Supply Chain",
        "subject": "Quote Request: AI Fleet Telematics, IoT Tracking & Dispatch Management System",
        "sender_name": "David Miller",
        "sender_email": "dmiller@transgloballogistics.com",
        "sender_company": "TransGlobal Logistics Corp",
        "sender_phone": "+1 (312) 555-4309",
        "body": """Hi Team,

TransGlobal Logistics operates a fleet of 350 heavy-duty trucks and 6 regional distribution hubs across North America. We need a modern, cloud-native Fleet Telematics and Dispatch Optimization platform.

Current pain points:
Our dispatchers currently use disconnected spreadsheets and phone calls, resulting in inefficient routes, high fuel costs, and poor delivery visibility for our corporate clients.

Scope of Work:
1. Real-time GPS Fleet Tracking: Ingest IoT telematics data from vehicle OBD-II / CAN-bus dongles every 5 seconds.
2. AI-Driven Dynamic Dispatch: Automatically sequence drops and calculate optimal routes considering traffic, vehicle weight, and driver duty hours (FMCSA ELD compliance).
3. Driver Mobile Application (iOS & Android): Turn-by-turn navigation, digital Proof of Delivery (e-signatures, barcode scanning of pallets, photo upload for damaged freight).
4. Customer Tracking Portal: Live consignment tracking link with dynamic ETA updates.
5. Maintenance & Fuel Telemetry: Automated diagnostic trouble code (DTC) alerts and preventative maintenance scheduling.

Integrations:
- Must connect to our existing SAP ERP for sales order ingestion.
- Integration with Geotab / Samsara telematics gateway.

We require a breakdown of development costs, testing and QA effort, ongoing infrastructure requirements, and clear deliverables.

Regards,
David Miller, Director of Operations
TransGlobal Logistics Corp
dmiller@transgloballogistics.com"""
    },
    {
        "id": "ecommerce_marketplace",
        "title": "E-Commerce: Multi-Vendor B2B/B2C Marketplace",
        "industry_hint": "E-Commerce & Retail",
        "subject": "RFP: High-Volume Multi-Vendor Luxury Lifestyle Marketplace with Real-time ERP Sync",
        "sender_name": "Elena Rostova",
        "sender_email": "elena.rostova@velvetandoak.com",
        "sender_company": "Velvet & Oak Lifestyle Brands",
        "sender_phone": "+1 (415) 555-9180",
        "body": """Dear Solutions Team,

Velvet & Oak is building a premier multi-vendor marketplace connecting independent artisan designers and luxury boutique brands with discerning buyers across North America and Western Europe.

Requirements Overview:
1. Customer Storefront: Lightning-fast, mobile-first responsive web catalog with faceted filtering, multi-angle zoom, and instant search powered by Elasticsearch.
2. Vendor Portal: Self-service onboarding for 200+ brands to manage product listings, inventory levels, order fulfillment, and commission payouts.
3. Omnichannel Checkout: Multi-currency checkout, automated sales tax / VAT calculation (Avalara), split-payments across multiple vendors in a single cart, and fraud prevention.
4. Promotional Engine: Tiered loyalty points, seasonal discount codes, gift cards, and automated abandoned cart recovery email sequences.
5. Logistics & Returns: Automated generation of pre-paid return shipping labels and tracking.

Scale & Performance:
- Must handle 10,000 concurrent shoppers during Black Friday / Cyber Monday flash sales without latency degradation.
- Integration with Shopify inventory feeds for vendors who prefer automated synchronization.

Please provide a detailed quotation including implementation phases, resource breakdown, milestone deliverables, and estimated turnaround time.

Kind regards,
Elena Rostova, VP of Digital Commerce
Velvet & Oak Lifestyle Brands
elena.rostova@velvetandoak.com"""
    },
    {
        "id": "edtech_lms",
        "title": "EdTech: Adaptive Learning & Video Platform",
        "industry_hint": "EdTech & E-Learning",
        "subject": "Tender Quotation: Adaptive Learning Management System with SCORM & Video Streaming",
        "sender_name": "Prof. Alan Grant",
        "sender_email": "agrant@horizonglobal.edu",
        "sender_company": "Horizon Global Academy",
        "sender_phone": "+1 (617) 555-3411",
        "body": """Hello,

Horizon Global Academy is seeking proposals for the development of our next-generation Adaptive Online Learning and Assessment Platform. We serve over 25,000 matriculated students worldwide.

Project Objectives:
- Deliver interactive video lectures with adaptive bitrate streaming, DRM protection, and timestamped bookmarks.
- Full compliance with SCORM 2004 4th Edition and xAPI standards so legacy course packages can be uploaded and played smoothly.
- Interactive quiz engine featuring auto-graded coding exercises, timed exams with anti-cheat lockdown, and peer-reviewed essay grading.
- Student analytics dashboard tracking mastery levels, time-on-task, and predicting at-risk students for early academic intervention.
- LTI 1.3 integration to allow single-sign-on (SSO) with existing institutional tools like Turnitin and Canvas.

Security & Compliance:
- Full compliance with FERPA and COPPA student privacy regulations.

Please provide an engineering quote outlining team roles, hours, development milestones, and itemized costs.

Sincerely,
Prof. Alan Grant, Dean of Digital Education
Horizon Global Academy
agrant@horizonglobal.edu"""
    },
    {
        "id": "custom_agtech",
        "title": "AgTech (Custom/Unknown Industry): Autonomous Drone Farm Analytics",
        "industry_hint": "Precision Agriculture & Drone Robotics",
        "subject": "Quote Request: Autonomous Drone Multispectral Farm Survey & Soil Analysis Platform",
        "sender_name": "Chloe Green",
        "sender_email": "chloe@terraaero.ag",
        "sender_company": "TerraAero Innovations",
        "sender_phone": "+1 (509) 555-8290",
        "body": """Hi QuoteFlow,

TerraAero develops autonomous aerial robotic systems for commercial agricultural enterprises. We need a software platform that processes multispectral aerial imagery captured by our fleet of fixed-wing agricultural survey drones.

System Requirements:
1. Drone Flight Data Ingestion: Secure upload of geo-tagged TIFF and raw infrared imagery from drone ground stations.
2. Orthomosaic Photogrammetry Pipeline: Cloud processing to stitch raw aerial images into high-resolution Normalized Difference Vegetation Index (NDVI) crop health maps.
3. AI Crop Stress & Disease Detection: Computer vision models to identify nitrogen deficiency, water stress, and weed infestation clusters across 5,000+ acre parcels.
4. Tractor Variable-Rate Prescription Export: Generate prescription shapefiles (.SHP and ISO-XML) that can be loaded into John Deere and Case IH tractor guidance monitors for targeted fertilizer spraying.
5. Offline Field Scout Mobile App: Allows agronomists to navigate to tagged problem zones in the field without cellular connectivity.

Can you formulate a comprehensive quotation covering engineering phases, cloud infrastructure estimates for heavy GPU photogrammetry processing, team roles, and milestone delivery?

Warm regards,
Chloe Green, Co-Founder & CTO
TerraAero Innovations
chloe@terraaero.ag"""
    }
]

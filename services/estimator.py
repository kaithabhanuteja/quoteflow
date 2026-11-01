"""
Deterministic Python Cost Estimation and Project Timeline Engine.
Calculates realistic resource allocations, working days, itemized costs,
contingency buffers, taxes, and payment milestones.
Never generates arbitrary or random figures.
"""

from typing import Dict, List, Any
import math
from services.industry_config import get_industry_profile


def format_inr(amount, include_symbol: bool = True, decimals: int = 2) -> str:
    """
    Formats a numeric value using the standard Indian numbering system.
    e.g. 150000 -> ₹1,50,000.00 (or ₹1,50,000 if decimals=0)
         1250000 -> ₹12,50,000.00
    """
    if amount is None:
        return "₹0.00" if include_symbol else "0.00"
    try:
        val = float(amount)
    except (ValueError, TypeError):
        return f"₹{amount}" if include_symbol else str(amount)
        
    is_negative = val < 0
    val = abs(val)
    
    if decimals > 0:
        base_str = f"{val:.{decimals}f}"
        int_part, dec_part = base_str.split(".")
        dec_part = "." + dec_part
    else:
        int_part = str(int(round(val)))
        dec_part = ""
        
    if len(int_part) <= 3:
        formatted_int = int_part
    else:
        last_three = int_part[-3:]
        remaining = int_part[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted_int = ",".join(groups) + "," + last_three
        
    res = ("-" if is_negative else "") + formatted_int + dec_part
    return f"₹{res}" if include_symbol else res


# Standard Professional Consulting Hourly Rate Card
BASE_RATE_CARD = {
    "solution_architect": {"title": "Principal Solution Architect", "seniority": "Principal / Lead", "rate": 125.0},
    "senior_fullstack": {"title": "Senior Full-Stack Engineer", "seniority": "Senior (6+ yrs)", "rate": 95.0},
    "mid_fullstack": {"title": "Full-Stack Software Engineer", "seniority": "Mid-Level (3-5 yrs)", "rate": 80.0},
    "ui_ux_designer": {"title": "Senior UI/UX & Design Systems Lead", "seniority": "Senior", "rate": 75.0},
    "qa_automation": {"title": "QA Automation & Security Engineer", "seniority": "Senior", "rate": 70.0},
    "devops_cloud": {"title": "DevOps & Cloud Systems Architect", "seniority": "Senior", "rate": 95.0},
    "project_manager": {"title": "Agile Project Manager / Scrum Lead", "seniority": "Senior", "rate": 80.0},
    "compliance_specialist": {"title": "Security & Regulatory Compliance Specialist", "seniority": "Lead", "rate": 115.0},
}


def calculate_project_estimates(
    analysis_data: Dict[str, Any],
    custom_overrides: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Computes an authoritative, mathematically sound project estimate
    based on the AI analysis results, complexity score, requirements count,
    and industry regulatory profile.
    
    Supports custom_overrides so users can interactively tweak rates, hours,
    contingency %, tax %, and discounts.
    """
    custom = custom_overrides or {}
    
    # 1. Base Variables from Analysis
    complexity_score = analysis_data.get("complexity", {}).get("score", 55)
    complexity_level = analysis_data.get("complexity", {}).get("level", "Medium")
    industry_name = analysis_data.get("industry", {}).get("industry_name", "General")
    requirements = analysis_data.get("requirements", [])
    integrations = analysis_data.get("integrations_detected", [])
    
    profile = get_industry_profile(industry_name)
    is_regulated = any(term in industry_name.lower() for term in ["health", "fintech", "banking", "finance"])
    
    req_count = max(4, len(requirements))
    int_count = max(1, len(integrations))

    # Complexity scale factor (0.85 for low complexity up to 1.55 for enterprise)
    complexity_factor = 0.85 + (complexity_score / 100.0) * 0.70

    # 2. Phase-wise Effort Calculation (Hours)
    # Phase 1: Inception & Architecture
    p1_hours = custom.get("phase_1_hours") or int(round((70 + (req_count * 5) + (15 if is_regulated else 0)) * (complexity_factor * 0.9)))
    
    # Phase 2: UI/UX & Interaction Design
    p2_hours = custom.get("phase_2_hours") or int(round((80 + (req_count * 7)) * (complexity_factor * 0.85)))
    
    # Phase 3: Core Functional Development
    p3_hours = custom.get("phase_3_hours") or int(round((200 + (req_count * 25)) * complexity_factor))
    
    # Phase 4: Integrations & API Middleware
    p4_hours = custom.get("phase_4_hours") or int(round((60 + (int_count * 35)) * complexity_factor))
    
    # Phase 5: QA, Security & Performance Testing
    p5_hours = custom.get("phase_5_hours") or int(round((90 + (req_count * 10) + (30 if is_regulated else 0)) * (complexity_factor * 0.95)))
    
    # Phase 6: Cloud Deployment & CI/CD Staging
    p6_hours = custom.get("phase_6_hours") or int(round((50 + (int_count * 10)) * complexity_factor))
    
    # Phase 7: UAT & 90-Day Post-Launch Hypercare
    p7_hours = custom.get("phase_7_hours") or int(round(40 + (req_count * 3)))

    total_project_hours = p1_hours + p2_hours + p3_hours + p4_hours + p5_hours + p6_hours + p7_hours

    # 3. Phases Structure for Presentation
    phases = [
        {
            "phase_number": 1,
            "name": f"{profile.get('code', 'DEV')}-P1: Inception, Discovery & Solution Architecture",
            "hours": p1_hours,
            "weeks": max(2, int(math.ceil(p1_hours / 40.0))),
            "deliverables": [
                "Technical Architecture Design Document (TADD)",
                "Data Models, Entity-Relationship Schemas & API Specifications",
                "Regulatory Compliance Matrix & Security Blueprint"
            ]
        },
        {
            "phase_number": 2,
            "name": f"{profile.get('code', 'DEV')}-P2: UI/UX Design System & Interactive Prototypes",
            "hours": p2_hours,
            "weeks": max(2, int(math.ceil(p2_hours / 45.0))),
            "deliverables": [
                "Comprehensive Figma Design System & Component Library",
                "Mobile & Desktop Responsive Wireframes",
                "Clickable Interactive Prototype for User Journey Validation"
            ]
        },
        {
            "phase_number": 3,
            "name": f"{profile.get('code', 'DEV')}-P3: Core Functional Engine & Backend Business Logic",
            "hours": p3_hours,
            "weeks": max(4, int(math.ceil(p3_hours / 80.0))),
            "deliverables": [
                "Core Database Schemas with Automated Migration Scripts",
                "REST / GraphQL API Endpoints with Automated Swagger Documentation",
                "Role-Based Access Control (RBAC) & Authentication Module"
            ]
        },
        {
            "phase_number": 4,
            "name": f"{profile.get('code', 'DEV')}-P4: Third-Party Integrations & Middleware Sync",
            "hours": p4_hours,
            "weeks": max(3, int(math.ceil(p4_hours / 60.0))),
            "deliverables": [
                f"Connector pipelines for {', '.join(integrations[:3]) if integrations else 'Core APIs'}",
                "Automated Webhook Ingestion & Dead-Letter Queue Error Handling",
                "Data Reconciliation & Integrity Health Monitor"
            ]
        },
        {
            "phase_number": 5,
            "name": f"{profile.get('code', 'DEV')}-P5: QA Automation, Security Audit & Load Testing",
            "hours": p5_hours,
            "weeks": max(2, int(math.ceil(p5_hours / 50.0))),
            "deliverables": [
                "Automated End-to-End Test Suite (>85% code coverage)",
                "Vulnerability Scanning & Static Application Security Testing (SAST)",
                "Performance Load Simulation (Peak Concurrent Users)"
            ]
        },
        {
            "phase_number": 6,
            "name": f"{profile.get('code', 'DEV')}-P6: Cloud Infrastructure, CI/CD Pipeline & Launch",
            "weeks": max(2, int(math.ceil(p6_hours / 40.0))),
            "hours": p6_hours,
            "deliverables": [
                "Infrastructure-as-Code (Terraform / CloudFormation)",
                "Automated Zero-Downtime GitHub Actions CI/CD Pipeline",
                "Production Go-Live & DNS Cutover Execution"
            ]
        },
        {
            "phase_number": 7,
            "name": f"{profile.get('code', 'DEV')}-P7: UAT Handover, Training & 90-Day Hypercare",
            "hours": p7_hours,
            "weeks": max(2, int(math.ceil(p7_hours / 30.0))),
            "deliverables": [
                "Stakeholder Handover, Administrator Training & Knowledge Base",
                "Full Source Code Transfer & IP Assignment",
                "90-Day Post-Launch Priority Defect Hypercare Warranty"
            ]
        }
    ]

    # 4. Resource Allocation & Team Composition
    # Map phase hours to specialized roles
    arch_hours = int(round(p1_hours * 0.70 + p6_hours * 0.25))
    designer_hours = int(round(p2_hours * 0.90 + p1_hours * 0.15))
    sr_dev_hours = int(round(p3_hours * 0.60 + p4_hours * 0.60 + p6_hours * 0.25))
    mid_dev_hours = int(round(p3_hours * 0.40 + p4_hours * 0.40))
    qa_hours = int(round(p5_hours * 0.85 + p3_hours * 0.10))
    devops_hours = int(round(p6_hours * 0.65 + p1_hours * 0.15))
    pm_hours = int(round(total_project_hours * 0.11))
    comp_hours = int(round((p1_hours + p5_hours) * 0.25)) if is_regulated else 0

    rates = custom.get("rates", {})
    r_arch = rates.get("solution_architect", BASE_RATE_CARD["solution_architect"]["rate"])
    r_sr_dev = rates.get("senior_fullstack", BASE_RATE_CARD["senior_fullstack"]["rate"])
    r_mid_dev = rates.get("mid_fullstack", BASE_RATE_CARD["mid_fullstack"]["rate"])
    r_designer = rates.get("ui_ux_designer", BASE_RATE_CARD["ui_ux_designer"]["rate"])
    r_qa = rates.get("qa_automation", BASE_RATE_CARD["qa_automation"]["rate"])
    r_devops = rates.get("devops_cloud", BASE_RATE_CARD["devops_cloud"]["rate"])
    r_pm = rates.get("project_manager", BASE_RATE_CARD["project_manager"]["rate"])
    r_comp = rates.get("compliance_specialist", BASE_RATE_CARD["compliance_specialist"]["rate"])

    team = [
        {
            "role": "Principal Solution Architect",
            "seniority": "Principal / Lead",
            "headcount": 1,
            "hours": arch_hours,
            "rate": r_arch,
            "cost": round(arch_hours * r_arch, 2),
            "responsibility": "System topology, data modeling, API contracts, and security architecture."
        },
        {
            "role": "Senior UI/UX Design Lead",
            "seniority": "Senior (6+ yrs)",
            "headcount": 1,
            "hours": designer_hours,
            "rate": r_designer,
            "cost": round(designer_hours * r_designer, 2),
            "responsibility": "Figma design system, high-fidelity prototypes, user journeys."
        },
        {
            "role": "Senior Full-Stack Engineers",
            "seniority": "Senior (6+ yrs)",
            "headcount": 2,
            "hours": sr_dev_hours,
            "rate": r_sr_dev,
            "cost": round(sr_dev_hours * r_sr_dev, 2),
            "responsibility": "Core backend business logic, integration middleware, frontend implementation."
        },
        {
            "role": "Full-Stack Software Engineers",
            "seniority": "Mid-Level (3-5 yrs)",
            "headcount": 1,
            "hours": mid_dev_hours,
            "rate": r_mid_dev,
            "cost": round(mid_dev_hours * r_mid_dev, 2),
            "responsibility": "Feature implementation, API endpoints, responsive UI integration."
        },
        {
            "role": "QA Automation & Security Engineer",
            "seniority": "Senior (5+ yrs)",
            "headcount": 1,
            "hours": qa_hours,
            "rate": r_qa,
            "cost": round(qa_hours * r_qa, 2),
            "responsibility": "Automated regression tests, API testing, SAST security vulnerability scanning."
        },
        {
            "role": "DevOps & Cloud Systems Architect",
            "seniority": "Senior",
            "headcount": 1,
            "hours": devops_hours,
            "rate": r_devops,
            "cost": round(devops_hours * r_devops, 2),
            "responsibility": "Multi-region cloud infrastructure, Terraform IaC, Docker, CI/CD pipelines."
        },
        {
            "role": "Agile Project Manager / Scrum Lead",
            "seniority": "Senior (PMP / CSM)",
            "headcount": 1,
            "hours": pm_hours,
            "rate": r_pm,
            "cost": round(pm_hours * r_pm, 2),
            "responsibility": "Sprint planning, stakeholder demo cadence, risk management, and governance."
        }
    ]

    if is_regulated and comp_hours > 0:
        team.append({
            "role": "Security & Regulatory Compliance Specialist",
            "seniority": "Industry Lead",
            "headcount": 1,
            "hours": comp_hours,
            "rate": r_comp,
            "cost": round(comp_hours * r_comp, 2),
            "responsibility": f"Audit verification for {profile.get('compliance_standards', ['Compliance'])[0]}."
        })

    total_team_cost = sum(member["cost"] for member in team)
    total_allocated_hours = sum(member["hours"] for member in team)

    # 5. Timeline & Calendar Duration Calculation
    # Concurrency factor: Team works in parallel across architecture, design, dev, and testing
    concurrency_engineers = 2.6  # Effective simultaneous full-time velocity
    working_days = int(math.ceil(total_project_hours / (8.0 * concurrency_engineers)))
    calendar_weeks = int(math.ceil(working_days / 5.0))
    # Add buffer for reviews and milestone signoffs
    total_delivery_weeks = max(8, calendar_weeks)

    # 6. Itemized Cost Breakdown
    dev_cost = round(sr_dev_hours * r_sr_dev + mid_dev_hours * r_mid_dev, 2)
    integration_cost = round(p4_hours * r_sr_dev, 2)
    qa_cost = round(qa_hours * r_qa, 2)
    design_cost = round(designer_hours * r_designer, 2)
    devops_cost = round(devops_hours * r_devops, 2)
    pm_cost = round(pm_hours * r_pm, 2)
    arch_cost = round(arch_hours * r_arch, 2)
    compliance_cost = round(comp_hours * r_comp, 2) if is_regulated else 0.0

    # Cloud infrastructure, staging environments & software tooling during project
    duration_months = max(2, int(math.ceil(total_delivery_weeks / 4.3)))
    monthly_infra_est = 650.0 if not is_regulated else 1150.0  # HIPAA/PCI environments cost more
    infra_setup_and_staging = round(duration_months * monthly_infra_est + 800.0, 2)

    subtotal = round(
        dev_cost + integration_cost + qa_cost + design_cost + 
        devops_cost + pm_cost + arch_cost + compliance_cost + infra_setup_and_staging, 
        2
    )

    # Contingency & Taxes
    contingency_pct = custom.get("contingency_percentage", 0.10)  # Default 10%
    tax_pct = custom.get("tax_percentage", 0.18)                  # Default 18%
    discount_amount = custom.get("discount_amount", 0.0)

    contingency_cost = round(subtotal * contingency_pct, 2)
    taxable_amount = round(subtotal + contingency_cost - discount_amount, 2)
    tax_cost = round(taxable_amount * tax_pct, 2)
    grand_total = round(taxable_amount + tax_cost, 2)

    # 7. Payment Milestones (Structured 4-Tranche Distribution)
    milestones = [
        {
            "milestone": "M1: Project Mobilization & Inception Sign-Off",
            "percentage": 25,
            "amount": round(grand_total * 0.25, 2),
            "trigger": "Contract execution, sprint zero kickoff, architecture blueprint approval."
        },
        {
            "milestone": "M2: Design Prototype & Alpha Core Engine",
            "percentage": 25,
            "amount": round(grand_total * 0.25, 2),
            "trigger": "Figma design system sign-off and functional Alpha release demonstration."
        },
        {
            "milestone": "M3: Third-Party Integrations & Beta Deployment",
            "percentage": 25,
            "amount": round(grand_total * 0.25, 2),
            "trigger": "Integration pipeline verification and staging environment deployment."
        },
        {
            "milestone": "M4: Security Audit, Final UAT & Production Launch",
            "percentage": 25,
            "amount": round(grand_total - (round(grand_total * 0.25, 2) * 3), 2),  # Exact penny balance
            "trigger": "Successful UAT acceptance, security sign-off, production launch, and IP transfer."
        }
    ]

    # 8. Estimation Methodology Explanation
    methodology_explanation = (
        f"This estimate is deterministically calculated using our Senior Engineering Effort Matrix. "
        f"The project complexity score ({complexity_score}/100, {complexity_level}) and requirement volume "
        f"({req_count} functional/technical items, {int_count} third-party integration points) yielded a total of "
        f"{total_allocated_hours} billable engineering hours across 7 phases. "
        f"With an active parallel team concurrency of {concurrency_engineers:.1f} developers, the projected delivery "
        f"timeline is {working_days} working days ({total_delivery_weeks} calendar weeks). "
        f"Subtotal cost is {format_inr(subtotal)}, backed by a {int(contingency_pct*100)}% risk contingency ({format_inr(contingency_cost)}) "
        f"and {int(tax_pct*100)}% applicable GST / Tax ({format_inr(tax_cost)}), resulting in a grand total of {format_inr(grand_total)}."
    )

    return {
        "complexity_level": complexity_level,
        "complexity_score": complexity_score,
        "total_hours": total_allocated_hours,
        "working_days": working_days,
        "delivery_weeks": total_delivery_weeks,
        "team_size": sum(m["headcount"] for m in team),
        "team_allocation": team,
        "phases": phases,
        "cost_breakdown": {
            "development_cost": dev_cost,
            "integration_cost": integration_cost,
            "design_cost": design_cost,
            "qa_testing_cost": qa_cost,
            "devops_cloud_cost": devops_cost,
            "project_management_cost": pm_cost,
            "architecture_cost": arch_cost,
            "compliance_cost": compliance_cost,
            "infrastructure_staging_cost": infra_setup_and_staging,
            "subtotal": subtotal,
            "contingency_percentage": contingency_pct,
            "contingency_cost": contingency_cost,
            "discount_amount": discount_amount,
            "tax_percentage": tax_pct,
            "tax_cost": tax_cost,
            "grand_total": grand_total,
            "currency": "INR"
        },
        "payment_milestones": milestones,
        "methodology_explanation": methodology_explanation
    }

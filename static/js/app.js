/**
 * Quotflow - Core Interactive Front-End Controller
 * Developed by Kaitha Bhanuteja for Quotflow Technologies Limited.
 * Handles email analysis, real-time estimation tweaking, PDF generation, and dashboard actions.
 */

// Global State
let currentAnalysis = null;
let currentEstimates = null;
let currentQuotation = null;
let rawEmailText = "";

document.addEventListener("DOMContentLoaded", function () {
    initSampleSelector();
    initEstimationEditor();
});

/**
 * Standard Indian Numbering System Currency Formatter
 * e.g. 150000 -> ₹1,50,000.00 | 1250000 -> ₹12,50,000.00
 */
function formatINR(val, includeSymbol = true, decimals = 2) {
    if (val === null || val === undefined || isNaN(val)) {
        return includeSymbol ? "₹0.00" : "0.00";
    }
    val = Number(val);
    const isNegative = val < 0;
    val = Math.abs(val);

    let parts;
    if (decimals > 0) {
        parts = val.toFixed(decimals).split(".");
    } else {
        parts = [Math.round(val).toString()];
    }

    let intPart = parts[0];
    let decPart = parts.length > 1 ? "." + parts[1] : "";

    let formattedInt = "";
    if (intPart.length <= 3) {
        formattedInt = intPart;
    } else {
        let lastThree = intPart.substring(intPart.length - 3);
        let remaining = intPart.substring(0, intPart.length - 3);
        let groups = [];
        while (remaining.length > 2) {
            groups.unshift(remaining.substring(remaining.length - 2));
            remaining = remaining.substring(0, remaining.length - 2);
        }
        if (remaining.length > 0) {
            groups.unshift(remaining);
        }
        formattedInt = groups.join(",") + "," + lastThree;
    }

    const res = (isNegative ? "-" : "") + formattedInt + decPart;
    return includeSymbol ? "₹" + res : res;
}

/**
 * Initialize sample email buttons
 */
function initSampleSelector() {
    const samplePills = document.querySelectorAll(".sample-pill-btn");
    const emailTextarea = document.getElementById("emailInput");

    samplePills.forEach(pill => {
        pill.addEventListener("click", function () {
            samplePills.forEach(p => p.classList.remove("active"));
            this.classList.add("active");

            const sampleBody = this.getAttribute("data-body");
            if (emailTextarea && sampleBody) {
                emailTextarea.value = sampleBody;
                rawEmailText = sampleBody;
                // Animate textarea briefly to indicate fill
                emailTextarea.classList.add("border-primary");
                setTimeout(() => emailTextarea.classList.remove("border-primary"), 400);
            }
        });
    });

    // Pick first sample by default if empty
    if (emailTextarea && !emailTextarea.value.trim() && samplePills.length > 0) {
        samplePills[0].click();
    }
}

/**
 * Step 1: Analyze Email with Gemini AI
 */
async function triggerEmailAnalysis() {
    const emailInput = document.getElementById("emailInput");
    const emailText = emailInput ? emailInput.value.trim() : "";
    const apiKeyInput = document.getElementById("geminiApiKeyInput");
    const customApiKey = apiKeyInput ? apiKeyInput.value.trim() : "";

    if (!emailText) {
        alert("Please enter or select a customer email to analyze.");
        return;
    }

    rawEmailText = emailText;

    // Show loading state
    const btn = document.getElementById("btnAnalyzeEmail");
    const originalBtnHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span> Analyzing with Gemini AI...`;

    const progressContainer = document.getElementById("analysisProgress");
    if (progressContainer) progressContainer.classList.remove("d-none");

    const statusText = document.getElementById("analysisStatusText");
    const steps = [
        "Ingesting customer inquiry email...",
        "Automatically identifying industry domain & compliance...",
        "Extracting confirmed requirements vs AI assumptions...",
        "Formulating clarification questions for missing information...",
        "Evaluating architectural complexity & calculating effort..."
    ];

    let stepIdx = 0;
    const interval = setInterval(() => {
        if (statusText && stepIdx < steps.length) {
            statusText.innerText = steps[stepIdx];
            stepIdx++;
        }
    }, 450);

    try {
        const response = await fetch("/api/analyze-email", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email_text: emailText,
                gemini_api_key: customApiKey
            })
        });

        clearInterval(interval);
        const data = await response.json();

        if (data.status === "success" && data.analysis) {
            currentAnalysis = data.analysis;
            renderAnalysisSection(currentAnalysis);
            
            // Automatically calculate baseline estimates
            await calculateEstimates();

            // Smooth scroll to analysis section
            const target = document.getElementById("step2Section");
            if (target) {
                target.classList.remove("d-none");
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }

            // Update step indicator
            updateStepIndicator(2);
        } else {
            alert("Analysis Error: " + (data.message || "Failed to analyze email."));
        }
    } catch (err) {
        clearInterval(interval);
        console.error(err);
        alert("Network or server error while analyzing email: " + err.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalBtnHtml;
        if (progressContainer) progressContainer.classList.add("d-none");
    }
}

/**
 * Render Step 2: Analysis Results
 */
function renderAnalysisSection(analysis) {
    const ind = analysis.industry || {};
    const cust = analysis.customer || {};
    const comp = analysis.complexity || {};

    // Industry and Complexity Badges
    document.getElementById("detectedIndustryName").innerText = ind.industry_name || "General";
    document.getElementById("detectedCategoryName").innerText = ind.category || "Custom Solution";
    document.getElementById("detectedConfidence").innerText = `${ind.confidence_score || 90}% Confidence`;
    document.getElementById("industryReasoning").innerText = ind.reasoning || "";

    const compBadge = document.getElementById("complexityBadge");
    const compScore = comp.score || 50;
    compBadge.innerText = `${comp.level || 'Medium'} (${compScore}/100)`;
    compBadge.className = "badge badge-complexity " + (
        compScore >= 80 ? "badge-complexity-enterprise" :
        compScore >= 65 ? "badge-complexity-high" :
        compScore >= 45 ? "badge-complexity-medium" : "badge-complexity-low"
    );

    // Customer Card
    document.getElementById("custName").innerText = cust.name || "Client Lead";
    document.getElementById("custCompany").innerText = cust.company || "Client Org";
    document.getElementById("custEmail").innerText = cust.email || "N/A";
    document.getElementById("custPhone").innerText = cust.phone || "N/A";
    document.getElementById("custRole").innerText = cust.designation || "Stakeholder";

    // Business Objectives
    document.getElementById("businessObjectivesText").innerText = analysis.business_objectives || "";

    // Requirements Matrix (Confirmed vs AI Assumptions)
    renderRequirementsTable(analysis.requirements || []);

    // Clarification Questions
    renderClarificationQuestions(analysis.clarification_questions || []);

    // Technical Stack & Integrations
    renderTechAndIntegrations(analysis.technical_stack_suggestions || [], analysis.integrations_detected || []);
}

/**
 * Render Requirements Table with Confirmed vs Assumptions Filter
 */
function renderRequirementsTable(reqs) {
    const tbody = document.getElementById("requirementsTableBody");
    if (!tbody) return;

    tbody.innerHTML = "";
    reqs.forEach(r => {
        const tr = document.createElement("tr");
        const isConfirmed = r.is_confirmed;
        const tagHtml = isConfirmed
            ? `<span class="badge-confirmed"><i class="bi bi-check-circle-fill me-1"></i> Confirmed</span>`
            : `<span class="badge-assumption"><i class="bi bi-stars me-1"></i> AI Assumption</span>`;

        tr.innerHTML = `
            <td class="font-mono text-muted" style="width: 85px;">${r.id}</td>
            <td style="width: 140px;">${tagHtml}</td>
            <td>
                <div class="fw-semibold text-dark">${escapeHtml(r.title)}</div>
                <div class="small text-secondary mt-1">${escapeHtml(r.description)}</div>
                ${r.source_reference ? `<div class="small text-muted font-italic mt-1" style="font-size: 0.78rem;"><i class="bi bi-chat-quote me-1"></i>"${escapeHtml(r.source_reference)}"</div>` : ''}
            </td>
            <td style="width: 130px;"><span class="badge bg-light text-dark border px-2 py-1">${escapeHtml(r.category)}</span></td>
        `;
        tbody.appendChild(tr);
    });

    const confirmedCount = reqs.filter(r => r.is_confirmed).length;
    const assumptionCount = reqs.length - confirmedCount;
    document.getElementById("confirmedCountBadge").innerText = `${confirmedCount} Confirmed`;
    document.getElementById("assumptionCountBadge").innerText = `${assumptionCount} AI Inferred`;
}

/**
 * Render Clarification Questions
 */
function renderClarificationQuestions(questions) {
    const container = document.getElementById("clarificationContainer");
    if (!container) return;

    if (!questions || questions.length === 0) {
        container.innerHTML = `<p class="text-muted small">No critical missing information detected.</p>`;
        return;
    }

    let html = `<div class="accordion" id="accordionQuestions">`;
    questions.forEach((q, idx) => {
        html += `
            <div class="accordion-item border-light mb-2 rounded overflow-hidden">
                <h2 class="accordion-header" id="headingQ${idx}">
                    <button class="accordion-button collapsed py-2 px-3 small fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#collapseQ${idx}">
                        <span class="badge bg-secondary me-2">${q.id || 'QST'}</span> ${escapeHtml(q.question)}
                    </button>
                </h2>
                <div id="collapseQ${idx}" class="accordion-collapse collapse" data-bs-parent="#accordionQuestions">
                    <div class="accordion-body small bg-light py-2 px-3">
                        <div class="text-muted mb-1"><strong>Why Essential:</strong> ${escapeHtml(q.why_needed)}</div>
                        <div class="text-primary"><strong>Baseline Quotation Assumption:</strong> ${escapeHtml(q.suggested_default)}</div>
                    </div>
                </div>
            </div>
        `;
    });
    html += `</div>`;
    container.innerHTML = html;
}

/**
 * Render Tech Stack & Integrations Pills
 */
function renderTechAndIntegrations(techStack, integrations) {
    const techBox = document.getElementById("techStackPills");
    const intBox = document.getElementById("integrationsPills");

    if (techBox) {
        techBox.innerHTML = techStack.map(t => 
            `<span class="badge bg-light text-dark border px-2 py-1"><i class="bi bi-layers me-1 text-primary"></i>${escapeHtml(t)}</span>`
        ).join(" ");
    }

    if (intBox) {
        intBox.innerHTML = integrations.map(i => 
            `<span class="badge bg-light text-dark border px-2 py-1"><i class="bi bi-plugin me-1 text-success"></i>${escapeHtml(i)}</span>`
        ).join(" ");
    }
}

/**
 * Step 3: Compute Estimates
 */
async function calculateEstimates(customOverrides = {}) {
    if (!currentAnalysis) return;

    try {
        const response = await fetch("/api/estimate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                analysis: currentAnalysis,
                custom_overrides: customOverrides
            })
        });

        const data = await response.json();
        if (data.status === "success" && data.estimates) {
            currentEstimates = data.estimates;
            renderEstimatesSection(currentEstimates);

            const target = document.getElementById("step3Section");
            if (target) {
                target.classList.remove("d-none");
            }
            updateStepIndicator(3);
        } else {
            console.error("Estimation failed:", data.message);
        }
    } catch (err) {
        console.error("Error computing estimates:", err);
    }
}

/**
 * Render Step 3: Estimates, Phases, Team, Financials (with Indian Rupee formatting)
 */
function renderEstimatesSection(estimates) {
    const costs = estimates.cost_breakdown || {};

    // KPI Metrics in Indian Rupee format
    document.getElementById("kpiTotalHours").innerText = `${estimates.total_hours.toLocaleString()} hrs`;
    document.getElementById("kpiDeliveryWeeks").innerText = `${estimates.delivery_weeks} wks (${estimates.working_days} days)`;
    document.getElementById("kpiTeamSize").innerText = `${estimates.team_size} Specialists`;
    document.getElementById("kpiGrandTotal").innerText = formatINR(costs.grand_total);

    // Phases Table
    const phaseTbody = document.getElementById("phasesTableBody");
    if (phaseTbody) {
        phaseTbody.innerHTML = "";
        (estimates.phases || []).forEach(ph => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td class="fw-semibold text-dark">${escapeHtml(ph.name)}</td>
                <td class="font-mono">${ph.hours} hrs</td>
                <td>${ph.weeks} wks</td>
                <td class="small text-muted">${ph.deliverables.map(d => `• ${escapeHtml(d)}`).join("<br/>")}</td>
            `;
            phaseTbody.appendChild(tr);
        });
    }

    // Team Table with Indian Rupee formatting
    const teamTbody = document.getElementById("teamTableBody");
    if (teamTbody) {
        teamTbody.innerHTML = "";
        (estimates.team_allocation || []).forEach(m => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td class="fw-semibold">${escapeHtml(m.role)}</td>
                <td class="small text-muted">${escapeHtml(m.seniority)}</td>
                <td class="text-center">${m.headcount}</td>
                <td class="font-mono">${m.hours} hrs</td>
                <td class="font-mono">${formatINR(m.rate)}/hr</td>
                <td class="font-mono fw-bold text-dark">${formatINR(m.cost)}</td>
            `;
            teamTbody.appendChild(tr);
        });
    }

    // Itemized Financial Ledger with Indian Rupee formatting
    const finTbody = document.getElementById("financialLedgerBody");
    if (finTbody) {
        const contingencyPct = Math.round((costs.contingency_percentage || 0.10) * 100);
        const taxPct = Math.round((costs.tax_percentage || 0.18) * 100);

        finTbody.innerHTML = `
            <tr>
                <td>Core Software Development</td>
                <td class="small text-muted">Senior and Mid Full-stack development hours</td>
                <td class="font-mono text-end">${formatINR(costs.development_cost)}</td>
            </tr>
            <tr>
                <td>Third-Party Integrations Middleware</td>
                <td class="small text-muted">API connectors, data pipelines, and error handling</td>
                <td class="font-mono text-end">${formatINR(costs.integration_cost)}</td>
            </tr>
            <tr>
                <td>UI/UX & Design Systems</td>
                <td class="small text-muted">Figma wireframes, component library, accessibility</td>
                <td class="font-mono text-end">${formatINR(costs.design_cost)}</td>
            </tr>
            <tr>
                <td>QA Automation & Security Audits</td>
                <td class="small text-muted">Automated test suites, vulnerability scans</td>
                <td class="font-mono text-end">${formatINR(costs.qa_testing_cost)}</td>
            </tr>
            <tr>
                <td>DevOps, Cloud Architecture & CI/CD</td>
                <td class="small text-muted">Terraform IaC, Docker staging clusters, pipelines</td>
                <td class="font-mono text-end">${formatINR(costs.devops_cloud_cost)}</td>
            </tr>
            <tr>
                <td>Agile Governance & Project Management</td>
                <td class="small text-muted">Scrum ceremonies, stakeholder demos, risk management</td>
                <td class="font-mono text-end">${formatINR(costs.project_management_cost)}</td>
            </tr>
            <tr>
                <td>Principal Solution Architecture</td>
                <td class="small text-muted">System blueprint, entity schemas, data modeling</td>
                <td class="font-mono text-end">${formatINR(costs.architecture_cost)}</td>
            </tr>
            ${costs.compliance_cost > 0 ? `
            <tr>
                <td>Security & Compliance Oversight</td>
                <td class="small text-muted">Domain regulatory verification & audits</td>
                <td class="font-mono text-end">${formatINR(costs.compliance_cost)}</td>
            </tr>` : ''}
            <tr>
                <td>Staging Cloud Infrastructure & Tooling</td>
                <td class="small text-muted">Cloud test environment & database instances</td>
                <td class="font-mono text-end">${formatINR(costs.infrastructure_staging_cost)}</td>
            </tr>
            <tr class="table-light fw-bold">
                <td>Base Engineering Subtotal</td>
                <td class="small text-muted">Direct engineering effort across all phases</td>
                <td class="font-mono text-end">${formatINR(costs.subtotal)}</td>
            </tr>
            <tr>
                <td>Contingency Risk Buffer (${contingencyPct}%)</td>
                <td class="small text-muted">Reserve for integration complexities & edge cases</td>
                <td class="font-mono text-end text-muted">${formatINR(costs.contingency_cost)}</td>
            </tr>
            ${costs.discount_amount > 0 ? `
            <tr class="text-success">
                <td>Commercial Courtesy Discount</td>
                <td class="small">Special initiative concession</td>
                <td class="font-mono text-end">-${formatINR(costs.discount_amount)}</td>
            </tr>` : ''}
            <tr>
                <td>Applicable GST / Taxes (${taxPct}%)</td>
                <td class="small text-muted">Standard commercial service tax assessment (18% GST)</td>
                <td class="font-mono text-end text-muted">${formatINR(costs.tax_cost)}</td>
            </tr>
            <tr class="table-primary border-primary fw-bold" style="font-size: 1.05rem;">
                <td>TOTAL PROJECT INVESTMENT (INR)</td>
                <td class="small">Guaranteed fixed-fee scope backed by Quotflow SLA</td>
                <td class="font-mono text-end text-primary">${formatINR(costs.grand_total)}</td>
            </tr>
        `;
    }

    // Payment Milestones with Indian Rupee formatting
    const mileTbody = document.getElementById("milestonesTableBody");
    if (mileTbody) {
        mileTbody.innerHTML = "";
        (estimates.payment_milestones || []).forEach(m => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td class="fw-semibold">${escapeHtml(m.milestone)}</td>
                <td class="small text-muted">${escapeHtml(m.trigger)}</td>
                <td class="text-center font-mono">${m.percentage}%</td>
                <td class="font-mono fw-bold text-end">${formatINR(m.amount)}</td>
            `;
            mileTbody.appendChild(tr);
        });
    }

    // Explanation Note
    document.getElementById("methodologyText").innerText = estimates.methodology_explanation || "";
}

/**
 * Initialize Interactive Estimation Editor Modal / Controls
 */
function initEstimationEditor() {
    const btnOpenEditor = document.getElementById("btnOpenEditor");
    const btnApplyOverrides = document.getElementById("btnApplyOverrides");

    if (btnOpenEditor) {
        btnOpenEditor.addEventListener("click", function () {
            // Populate current values into inputs
            if (!currentEstimates) return;
            const modal = new bootstrap.Modal(document.getElementById("editEstimatesModal"));
            modal.show();
        });
    }

    if (btnApplyOverrides) {
        btnApplyOverrides.addEventListener("click", async function () {
            const contingencyVal = parseFloat(document.getElementById("editContingencyInput").value) / 100.0;
            const taxVal = parseFloat(document.getElementById("editTaxInput").value) / 100.0;
            const discountVal = parseFloat(document.getElementById("editDiscountInput").value) || 0.0;

            const overrides = {
                contingency_percentage: isNaN(contingencyVal) ? 0.10 : contingencyVal,
                tax_percentage: isNaN(taxVal) ? 0.18 : taxVal,
                discount_amount: discountVal,
                rates: {
                    senior_fullstack: parseFloat(document.getElementById("editSrDevRate").value) || 95.0,
                    qa_automation: parseFloat(document.getElementById("editQaRate").value) || 70.0,
                    solution_architect: parseFloat(document.getElementById("editArchRate").value) || 125.0
                }
            };

            await calculateEstimates(overrides);

            // Hide modal
            const modalEl = document.getElementById("editEstimatesModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
        });
    }
}

/**
 * Step 4: Finalize Quotation and Generate PDF
 */
async function generateFinalQuotation() {
    if (!currentAnalysis || !currentEstimates) {
        alert("Please complete email analysis and estimation review first.");
        return;
    }

    const btn = document.getElementById("btnGenerateQuotation");
    const originalHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span> Generating PDF & Saving to Database...`;

    try {
        const response = await fetch("/api/quotations/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                analysis: currentAnalysis,
                estimates: currentEstimates,
                email_source: rawEmailText
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            currentQuotation = data;
            
            // Show Step 4 section
            const step4 = document.getElementById("step4Section");
            if (step4) {
                step4.classList.remove("d-none");
                step4.scrollIntoView({ behavior: "smooth" });
            }

            document.getElementById("successRefNo").innerText = data.reference_no;
            document.getElementById("successGrandTotal").innerText = `${formatINR(data.total_cost)} INR`;
            
            // Configure PDF download and preview buttons
            const downloadBtn = document.getElementById("btnDownloadPdf");
            if (downloadBtn) {
                downloadBtn.href = data.pdf_url;
            }

            const previewFrame = document.getElementById("pdfPreviewIframe");
            if (previewFrame) {
                previewFrame.src = data.preview_url;
            }

            const viewQuoteBtn = document.getElementById("btnViewQuoteDetail");
            if (viewQuoteBtn) {
                viewQuoteBtn.href = `/quotations/${data.quotation_id}`;
            }

            updateStepIndicator(4);
        } else {
            alert("Quotation Generation Error: " + (data.message || "Failed to create quotation."));
        }
    } catch (err) {
        console.error(err);
        alert("Server error while generating quotation PDF: " + err.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalHtml;
    }
}

/**
 * Quick Status Change in Dashboard
 */
async function updateQuotationStatus(quotationId, newStatus) {
    try {
        const response = await fetch(`/api/quotations/${quotationId}/status`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: newStatus })
        });
        const data = await response.json();
        if (data.status === "success") {
            window.location.reload();
        } else {
            alert("Status update failed: " + data.message);
        }
    } catch (err) {
        alert("Error updating status: " + err.message);
    }
}

/**
 * Update step navigation visual state
 */
function updateStepIndicator(activeStep) {
    for (let i = 1; i <= 4; i++) {
        const item = document.getElementById(`stepItem${i}`);
        if (!item) continue;

        item.classList.remove("active", "completed");
        if (i < activeStep) {
            item.classList.add("completed");
        } else if (i === activeStep) {
            item.classList.add("active");
        }
    }
}

/**
 * Utility: HTML Escape
 */
function escapeHtml(str) {
    if (!str) return "";
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

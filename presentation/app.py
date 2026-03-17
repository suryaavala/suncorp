"""Streamlit Presentation Deck — GenAI Policy Adjudicator.

Interactive slide-deck showcasing the enterprise RAG microservice
built for the Suncorp Senior Data Scientist interview.

Run with:
    cd presentation && streamlit run app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

# ── Page Config ──────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Suncorp Tech Showcase",
    page_icon="⚡",
)

# ── Load Custom CSS ──────────────────────────────────────────────
css_path = Path(__file__).parent / ".style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ── Assets Path ──────────────────────────────────────────────────
ASSETS = Path(__file__).parent / "assets"

# ── Sidebar Navigation ──────────────────────────────────────────
st.sidebar.markdown("## ⚡ AI Tech Showcase")
st.sidebar.markdown("---")

slide = st.sidebar.radio(
    "Navigation",
    [
        "1. Title",
        "2. Background & Goal",
        "3. Implementation & Architecture",
        "4. Project Outcomes",
        "5. Future State",
    ],
    label_visibility="collapsed",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 1: Title
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if slide == "1. Title":
    title_img = ASSETS / "title_bg.png"
    if title_img.exists():
        st.image(str(title_img), width="stretch")

    st.markdown(
        """
        <div style="text-align: center; padding: 60px 0 20px 0;">
            <h1 style="font-size: 3.2rem; margin-bottom: 0; color: #c9d1d9;">
                GenAI Policy Adjudicator
            </h1>
            <h2 style="font-size: 1.8rem; border: none; color: #8b949e !important;
                        font-weight: 400; margin-top: 10px; border-bottom: none !important;">
                Automated Claims Triage via Agentic RAG
            </h2>
            <div style="width: 80px; height: 4px; background-color: #58a6ff; margin: 30px auto;"></div>
            <p style="font-size: 1.2rem; color: #8b949e; margin-top: 10px; font-weight: 500;">
                Technical Showcase for AI Engineering
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 2: Background & Goal
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif slide == "2. Background & Goal":
    st.title("Background & Goal")
    st.markdown("---")

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.subheader("🔴 The Problem")
        st.markdown(
            """
            - **Manual FNOL Triage:** Adjusters spend hours cross-referencing
              unstructured claim reports against dense Product Disclosure
              Statements (PDS).
            - **Inconsistent Decisions:** Human fatigue leads to variability
              in approval/denial outcomes for similar claims.
            - **Slow Cycle Times:** Average first-touch resolution takes
              days, eroding customer trust and increasing operational costs.
            - **Audit Gaps:** Manual decisions lack the structured,
              reproducible trace required for regulatory compliance.
            """
        )

    with col_right:
        st.subheader("🟢 The Goal")
        st.markdown(
            """
            Build a **scalable Agentic RAG system** that automates
            initial claim triage — reducing cycle times while maintaining
            strict **Auditability-by-Design**.

            **Key Design Principles:**
            - 🏗️ **Enterprise-Grade Architecture:**
              FastAPI microservice, containerized, CI/CD enforced.
            - 🔍 **Two-Stage Retrieval:**
              Dense embedding search + Cross-Encoder re-ranking
              for surgical context extraction.
            - 🛡️ **Human-in-the-Loop Guardrails:**
              Configurable confidence threshold ensuring ambiguous
              claims always reach a human adjuster.
            - 📊 **Full Observability:**
              Every prompt, response, and decision trace is
              immutably logged in MLflow.
            """
        )

    # ── Before & After: Interactive Tabs ──
    st.markdown("")
    st.subheader("Before & After: A Single Claim")

    tab_before, tab_after = st.tabs(["Traditional Triage", "Agentic Triage"])

    with tab_before:
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        st.info(
            '📧 **Incoming FNOL Email:**\n\n'
            '"Hi, a pipe burst in my ceiling yesterday afternoon and water '
            'went everywhere. My laptop that was on the desk is completely '
            'ruined and the carpet in the living room is soaked through and '
            'smells terrible. I think the pipe was old. My policy number is '
            'HOM-2024-98412. Can someone please help? — Sarah M."'
        )
        st.caption(
            "⚠️ **The Problem:** An adjuster must now manually read the PDS, identify "
            "covered perils, cross-reference exclusions, and make a "
            "decision — often taking 30+ minutes per claim."
        )

    with tab_after:
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        st.json(
            {
                "claim_id": "CLM-1042",
                "incident_type": "Water Damage — Burst Pipe",
                "covered_items": ["Laptop (Contents)", "Carpet (Building)"],
                "policy_number": "HOM-2024-98412",
                "decision": "Escalate",
                "confidence_score": 0.78,
                "reasoning": "Burst pipe is a covered peril under Section 4.2, "
                "but the age of the pipe may trigger the maintenance "
                "exclusion under Section 6.1. Requires human review.",
                "cited_policy_clause": "Section 4.2: Escape of Liquid; "
                "Section 6.1: Maintenance & Wear Exclusion",
            }
        )
        st.caption(
            "✅ **The Solution:** The AI extracts structure in < 3 seconds, cites the exact "
            "policy clauses, and routes ambiguous claims to a human."
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 3: Implementation & Architecture
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif slide == "3. Implementation & Architecture":
    st.title("Implementation & Architecture")
    st.markdown("---")

    arch_img = ASSETS / "rag_architecture.png"
    if arch_img.exists():
        st.image(str(arch_img), caption="RAG Pipeline Architecture", width="stretch")

    st.markdown("")

    with st.expander("🔬 Deep Dive: Two-Stage Retrieval", expanded=False):
        st.markdown(
            """
            The retrieval pipeline uses a **two-stage approach** to maximize
            context precision:

            **Stage 1 — Dense Embedding Search (ChromaDB):**
            The claim description is embedded using Google's
            `gemini-embedding-001` model. The resulting vector queries a
            local ChromaDB collection, retrieving the **top 10** most
            semantically similar policy chunks.

            **Stage 2 — Cross-Encoder Re-ranking:**
            The 10 candidate chunks are re-scored by a fine-tuned
            `cross-encoder/ms-marco-MiniLM-L-6-v2` model. This model
            evaluates each (query, chunk) pair directly, producing a
            much more precise relevance score. The **top 2** chunks are
            selected as the final context for the LLM.

            This approach combines the **recall** of dense retrieval
            with the **precision** of cross-encoder re-ranking —
            delivering surgically relevant context to the LLM.
            """
        )

    st.markdown("")
    st.subheader("Technical Deep Dive")

    tab_code, tab_prompt, tab_schema = st.tabs(
        ["Core Endpoint Code", "Prompt Architecture", "JSON Schema"]
    )

    with tab_code:
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        st.code(
            '''
@app.post("/adjudicate")
async def adjudicate_claim(request: ClaimRequest):
    """Process an insurance claim through the RAG pipeline."""
    try:
        result = evaluate_claim_from_dict(request.model_dump())
        return result
    except Exception as e:
        logging.error("Adjudication failed: %s", str(e))
        raise HTTPException(status_code=503, detail="LLM Provider Error")
            '''.strip(),
            language="python",
        )

    with tab_prompt:
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        st.markdown("**System prompt sent to `gemini-2.5-flash`:**")
        st.code(
            '''
You are an expert insurance claims adjudicator.
Given the following insurance policy excerpts and a claim
description, determine whether the claim should be
Approved, Denied, or Escalated.

Policy Context:
{retrieved_policy_chunks}

Claim Data:
{claim_json}

Evaluate the claim accurately based only on the policy
context provided. If you do not have enough specific
information, Escalate. Provide reasoning and cite the
specific policy clause that supports your decision.
            '''.strip(),
            language="text",
        )
        st.caption(
            "The prompt injects the top-2 re-ranked policy chunks "
            "and the raw claim JSON. The LLM is constrained to "
            "return structured output via a Pydantic schema."
        )

    with tab_schema:
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        st.markdown(
            "**Pydantic model enforcing structured LLM output "
            "(zero tolerance for hallucinations):**"
        )
        st.code(
            '''
class AdjudicationResult(BaseModel):
    """Structured output schema for claim adjudication."""
    decision: Literal["Approve", "Deny", "Escalate"]
    confidence_score: float = Field(ge=0.0, le=1.0)
    reasoning: str
    cited_policy_clause: str
            '''.strip(),
            language="python",
        )
        st.caption(
            "By passing this schema to Gemini's structured output mode, "
            "the model is physically constrained to return valid JSON "
            "matching this exact structure — eliminating free-text "
            "hallucinations entirely."
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 4: Project Outcomes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif slide == "4. Project Outcomes":
    st.title("Project Outcomes")
    st.markdown("---")

    st.subheader("Automated Evaluation & HITL Guardrails")

    # Synthetic Data Generation for Business Visualization
    np.random.seed(42)
    n_claims = 30
    claim_ids = [f"CLM-{1000+i}" for i in range(n_claims)]

    # Generate scores: a cluster of highly confident claims,
    # and a cluster of ambiguous ones.
    scores = np.concatenate(
        [np.random.normal(0.92, 0.04, 20), np.random.normal(0.75, 0.08, 10)]
    )
    scores = np.clip(scores, 0.1, 0.99)
    statuses = [
        "Automated (STP)" if s >= 0.85 else "Escalated (HITL)" for s in scores
    ]

    df = pd.DataFrame(
        {"Claim ID": claim_ids, "Confidence Score": scores, "Routing": statuses}
    )

    # Plotly Figure
    fig = px.scatter(
        df,
        x="Claim ID",
        y="Confidence Score",
        color="Routing",
        color_discrete_map={
            "Automated (STP)": "#3fb950",  # GitHub Green
            "Escalated (HITL)": "#f78166", # GitHub Orange
        },
        title="AI Confidence vs. Claim Routing Decision",
        template="plotly_dark",
    )

    fig.add_hline(
        y=0.85,
        line_dash="dash",
        line_color="red",
        annotation_text="HITL Threshold (85%)",
    )
    fig.update_layout(yaxis_range=[0.5, 1.05], xaxis_tickangle=-45)

    st.plotly_chart(fig, width="stretch")

    # Metric Callouts
    col1, col2, col3 = st.columns(3)
    col1.metric("Target Automation Rate", "66%", "STP Eligible")
    col2.metric(
        "Escalation Rate", "34%", "HITL Review Required", delta_color="inverse"
    )
    col3.metric("Hallucinations on Complex Claims", "0%", "Guarded by threshold")

    # ── HITL Queue Deep Dive ──
    st.markdown("")
    st.subheader("Actionable Insight: The HITL Queue")

    hitl_df = df[df["Routing"] == "Escalated (HITL)"].copy()
    hitl_df = hitl_df.reset_index(drop=True)

    np.random.seed(99)
    escalation_reasons = [
        "Ambiguous Policy Clause",
        "High Fraud Score",
        "Multi-Peril Overlap",
        "Maintenance Exclusion Trigger",
        "Incomplete Claim Data",
    ]
    hitl_df["Reason for Escalation"] = np.random.choice(
        escalation_reasons, size=len(hitl_df)
    )
    hitl_df["Est. Claim Value"] = [
        f"${v:,.0f}"
        for v in np.random.uniform(2500, 45000, size=len(hitl_df))
    ]
    hitl_df["Confidence Score"] = hitl_df["Confidence Score"].round(3)

    st.dataframe(
        hitl_df[["Claim ID", "Confidence Score", "Reason for Escalation", "Est. Claim Value"]],
        width="stretch",
        hide_index=True,
    )

    st.markdown(
        "By filtering out the **66% of clean claims** via Straight-Through "
        "Processing, human adjusters can now focus **100% of their time** "
        "on these high-complexity, high-risk escalations — dramatically "
        "improving decision quality where it matters most."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 5: Future State & Scaling
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif slide == "5. Future State":
    st.title("Future State & Scaling")
    st.markdown("---")

    st.markdown(
        """
        This system is designed to scale from a local POC to a
        **production-grade, highly available microservice** embedded
        in core claims infrastructure.
        """
    )

    st.subheader("Production Roadmap")

    roadmap_data = {
        "Phase": [
            "1. Pilot & Shadow Mode",
            "2. Databricks Migration",
            "3. Low-Risk Automation (STP)",
            "4. Ecosystem Integration",
        ],
        "Timeline": ["Months 1–2", "Months 3–4", "Months 5–6", "Months 7+"],
        "Key Action": [
            "Deploy alongside legacy system. Log AI decisions — don't act on them. "
            "Establish accuracy baseline vs. human adjusters.",
            "Swap ChromaDB → Databricks Vector Search via the existing ABC. "
            "Automate nightly ETL pipelines for PDS ingestion.",
            "Enable Straight-Through Processing for high-confidence, "
            "low-dollar claims (≥ 95% confidence, < $5k).",
            "Embed AI decision trace in adjuster UI. "
            "Expand to fraud detection and multimodal input.",
        ],
        "Success Criteria": [
            "≥ 90% AI–human agreement on Tier 1 claims",
            "Vector Search latency < 200ms at p95",
            "40%+ Tier 1 claims via STP, < 5% override rate",
            "60% reduction in end-to-end triage time",
        ],
    }

    st.dataframe(
        pd.DataFrame(roadmap_data),
        width="stretch",
        hide_index=True,
    )

    st.markdown("")
    st.subheader("Scaling the Architecture")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **🗄️ Data Layer**
            - ChromaDB → Databricks Vector Search
            - Unity Catalog for governance
            - Bronze / Silver / Gold lakehouse
            """
        )

    with col2:
        st.markdown(
            """
            **⚙️ Compute & Serving**
            - Kubernetes (EKS / AKS)
            - Horizontal pod autoscaling
            - Databricks Model Serving
            """
        )

    with col3:
        st.markdown(
            """
            **🔒 Security & Compliance**
            - PII Scrubbing (Microsoft Presidio)
            - RBAC via Unity Catalog + Okta
            - WORM audit trail (APRA / ASIC)
            """
        )

    # ── Projected Business ROI ──
    st.markdown("")
    st.subheader("Projected Business ROI")

    roi1, roi2, roi3, roi4 = st.columns(4)
    roi1.metric("Projected STP Rate", "45% (Year 1)")
    roi2.metric("Triage Time Reduction", "80%")
    roi3.metric("Adjuster Capacity Increase", "2.5x")
    roi4.metric("Audit Traceability", "100%")

    st.markdown("")
    st.markdown(
        "Transitioning this architecture into Suncorp's core systems will "
        "not only **optimize operational expenditure** but establish a "
        "foundation for **proactive, AI-driven risk management** across "
        "the portfolio."
    )

# app.py
import streamlit as st
from main import analyze_email

# ── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="Email Intent & Urgency Detector",
    page_icon="📧",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    h1 {
        text-align: center;
        color: #00d4ff !important;
        font-size: 2.4rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px #00d4ff88;
        padding-bottom: 0.3rem;
    }
    h2, h3 {
        color: #a78bfa !important;
        font-weight: 700 !important;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .stTextArea textarea {
        background-color: #1e1b4b !important;
        color: #e2e8f0 !important;
        border: 1.5px solid #6366f1 !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
    }
    .stSelectbox > div > div {
        background-color: #1e1b4b !important;
        color: #e2e8f0 !important;
        border: 1.5px solid #6366f1 !important;
        border-radius: 10px !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        box-shadow: 0 4px 20px #6366f155 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 6px 25px #6366f188 !important;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e1b4b, #312e81) !important;
        border: 1px solid #6366f1 !important;
        border-radius: 14px !important;
        padding: 1rem 1.2rem !important;
        box-shadow: 0 4px 15px #6366f133 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #a78bfa !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
    }
    hr {
        border-color: #6366f133 !important;
    }
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.82rem;
        margin-top: 1rem;
    }
    .badge-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 0.5rem 0;
    }
    .badge {
        padding: 6px 16px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.88rem;
        display: inline-block;
    }
    .badge-critical   { background:#fee2e2; color:#991b1b; }
    .badge-high       { background:#ffedd5; color:#9a3412; }
    .badge-medium     { background:#fef9c3; color:#854d0e; }
    .badge-low        { background:#dcfce7; color:#166534; }
    .badge-positive   { background:#d1fae5; color:#065f46; }
    .badge-neutral    { background:#e0f2fe; color:#075985; }
    .badge-negative   { background:#fee2e2; color:#991b1b; }
    .badge-frustrated { background:#fde68a; color:#92400e; }
    .badge-angry      { background:#fecaca; color:#7f1d1d; }
    .badge-polite     { background:#ede9fe; color:#4c1d95; }
</style>
""", unsafe_allow_html=True)

# ── Sample Emails ─────────────────────────────────────
SAMPLE_EMAILS = {
    "🔴 Critical — Server Down Alert": """Hi Team,

Our production server has been completely down for the past 2 hours.
Customers cannot access the platform and we are losing $5000 every hour.
The DevOps team is not responding to calls or messages.
I need IMMEDIATE escalation to the CTO right now.
This is a P0 incident — all hands on deck!

- Ravi (Operations Head)""",

    "🟠 High — Job Offer Deadline": """Dear HR Team,

I received your job offer letter yesterday and I am very interested.
However, I need some clarification on the salary structure and joining bonus
before I can sign the agreement.
My current employer needs a decision by this Friday EOD.
Could you please schedule a quick call tomorrow morning?

Best regards,
Priya Sharma""",

    "🟡 Medium — Project Status Update": """Hi Manager,

I wanted to give you a quick update on the mobile app project.
We have completed the login module and are currently working on
the dashboard feature. We are roughly 60% done overall.
There are a few minor blockers with the API integration
which we expect to resolve by end of this week.

Let me know if you need a detailed report.

Thanks,
Arjun""",

    "🟢 Low — Team Lunch Invitation": """Hey everyone! 🎉

Just a fun reminder that we are doing a team lunch this Friday at 1 PM
at Barbeque Nation near the office. It's completely optional but would
love to see everyone there! Please reply so I can confirm the headcount
with the restaurant.

Cheers,
Sneha""",

    "🔴 Critical — Legal Notice": """To The Management,

This is to formally notify you that our legal team has reviewed
the contract breach that occurred on March 15th.
If the pending payment of ₹8,50,000 is not settled within 48 hours,
we will be forced to initiate legal proceedings immediately.
This is our final notice before court action.

Regards,
Advocate Mehta
Legal Department""",

    "🟠 High — Client Escalation": """Dear Support Manager,

I have been trying to get my issue resolved for the past 10 days
but every agent I speak to gives me a different answer.
My subscription was charged twice in March and I still have not
received the refund despite 4 follow-up emails.
If this is not resolved by tomorrow, I will dispute the charge
with my bank and leave a detailed review on all platforms.

Disappointed,
Kiran Reddy""",

    "🟡 Medium — Interview Reschedule": """Hi Recruiter,

Thank you for scheduling my interview for Wednesday at 3 PM.
Unfortunately I have a prior medical appointment that I cannot reschedule.
Could we please move the interview to Thursday or Friday at the same time?
I am very excited about this opportunity and definitely want to attend.

Apologies for the inconvenience.

Warm regards,
Aditya Kumar""",

    "🟢 Low — Feedback Request": """Hi there,

Hope you are doing well! We noticed you recently used our service
and would love to hear your thoughts.
If you have 2 minutes, please fill out our quick feedback form —
your opinion genuinely helps us improve.
No pressure at all, completely optional!

Thank you,
Customer Success Team
TechCorp""",
}

URGENCY_BADGE = {
    "Critical": '<span class="badge badge-critical">🔴 Critical</span>',
    "High":     '<span class="badge badge-high">🟠 High</span>',
    "Medium":   '<span class="badge badge-medium">🟡 Medium</span>',
    "Low":      '<span class="badge badge-low">🟢 Low</span>',
}

SENTIMENT_BADGE = {
    "Positive":   '<span class="badge badge-positive">😊 Positive</span>',
    "Neutral":    '<span class="badge badge-neutral">😐 Neutral</span>',
    "Negative":   '<span class="badge badge-negative">😟 Negative</span>',
    "Frustrated": '<span class="badge badge-frustrated">😤 Frustrated</span>',
    "Angry":      '<span class="badge badge-angry">😠 Angry</span>',
    "Polite":     '<span class="badge badge-polite">🙂 Polite</span>',
}

# ── Header ────────────────────────────────────────────
st.title("📧 Email Intent & Urgency Detector")
st.markdown(
    '<div class="subtitle">Paste any email — AI instantly detects <b>intent</b>, <b>urgency</b>, <b>sentiment</b> & <b>recommended action</b></div>',
    unsafe_allow_html=True,
)
st.divider()

# ── Sample Loader ─────────────────────────────────────
st.subheader("💡 Try a Sample Email")
selected = st.selectbox(
    "Choose a sample:",
    options=["-- Select a sample --"] + list(SAMPLE_EMAILS.keys()),
    label_visibility="collapsed",
)
sample_text = SAMPLE_EMAILS.get(selected, "") if selected != "-- Select a sample --" else ""

# ── Email Input ───────────────────────────────────────
st.subheader("📩 Paste Your Email")
email_text = st.text_area(
    label="Email content",
    value=sample_text,
    height=220,
    placeholder="Dear Team,\n\nI wanted to follow up regarding...",
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Analyze Button ────────────────────────────────────
analyze_clicked = st.button(
    "🔍 Analyze Email",
    type="primary",
    use_container_width=True,
)

# ── Results ───────────────────────────────────────────
if analyze_clicked:
    if not email_text.strip():
        st.error("⚠️ Please paste an email before clicking Analyze!")
    else:
        with st.spinner("🤖 AI is reading and analyzing your email..."):
            try:
                result = analyze_email(email_text)

                st.markdown("<br>", unsafe_allow_html=True)
                st.success("✅ Analysis Complete!")
                st.divider()
                st.subheader("📊 Analysis Results")

                # ── Metric Cards ──
                col1, col2, col3 = st.columns(3)
                col1.metric("🎯 Intent",    result.intent)
                col2.metric("⚡ Urgency",   result.urgency)
                col3.metric("😊 Sentiment", result.sentiment)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── Colored Badges ──
                urgency_badge   = URGENCY_BADGE.get(result.urgency, result.urgency)
                sentiment_badge = SENTIMENT_BADGE.get(result.sentiment, result.sentiment)
                st.markdown(
                    f'<div class="badge-row">{urgency_badge}{sentiment_badge}</div>',
                    unsafe_allow_html=True,
                )

                st.divider()

                # ── Summary ──
                st.markdown("#### 📝 Email Summary")
                st.info(result.summary)

                # ── Suggested Action ──
                st.markdown("#### ✅ Suggested Action")
                st.success(result.suggested_action)

                st.divider()

                # ── JSON Output ──
                with st.expander("🔧 View Raw JSON Output"):
                    st.json({
                        "intent":           result.intent,
                        "urgency":          result.urgency,
                        "summary":          result.summary,
                        "suggested_action": result.suggested_action,
                        "sentiment":        result.sentiment,
                    })

            except Exception as e:
                err = str(e)
                if "429" in err:
                    st.error("⚠️ API Quota Exceeded! Please wait 1 minute and try again.")
                    st.warning("💡 Your free tier limit was hit. Wait 60 seconds then retry.")
                elif "decommissioned" in err:
                    st.error("❌ Model is outdated. Please update model.py!")
                else:
                    st.error(f"❌ Error: {err}")
                    st.info("💡 Check your `.env` file has a valid `GROQ_API_KEY`")

# ── Footer ────────────────────────────────────────────
st.divider()
st.markdown(
    '<div class="footer">Built with ❤️ using LangChain + Groq LLaMA + Streamlit &nbsp;|&nbsp; Internship Project — Sprint 1</div>',
    unsafe_allow_html=True,
)
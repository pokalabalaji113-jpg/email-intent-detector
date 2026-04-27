# app.py
import streamlit as st
from main import analyze_with_retry

st.set_page_config(
    page_title="Email Intent & Urgency Detector",
    page_icon="📧",
    layout="centered",
)

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    h1 { text-align: center; color: #00d4ff !important; font-size: 2.4rem !important; font-weight: 900 !important; text-shadow: 0 0 20px #00d4ff88; }
    h2, h3 { color: #a78bfa !important; font-weight: 700 !important; }
    .subtitle { text-align: center; color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem; }
    .stTextArea textarea { background-color: #1e1b4b !important; color: #e2e8f0 !important; border: 1.5px solid #6366f1 !important; border-radius: 12px !important; }
    .stSelectbox > div > div { background-color: #1e1b4b !important; color: #e2e8f0 !important; border: 1.5px solid #6366f1 !important; border-radius: 10px !important; }
    .stButton > button[kind="primary"] { background: linear-gradient(90deg, #6366f1, #8b5cf6) !important; color: white !important; font-size: 1.1rem !important; font-weight: 700 !important; border: none !important; border-radius: 12px !important; }
    [data-testid="stMetric"] { background: linear-gradient(135deg, #1e1b4b, #312e81) !important; border: 1px solid #6366f1 !important; border-radius: 14px !important; padding: 1rem 1.2rem !important; }
    [data-testid="stMetricLabel"] { color: #a78bfa !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-weight: 800 !important; font-size: 1rem !important; }
    hr { border-color: #6366f133 !important; }
    .footer { text-align: center; color: #64748b; font-size: 0.82rem; margin-top: 1rem; }
    .badge-row { display: flex; gap: 10px; flex-wrap: wrap; margin: 0.5rem 0; }
    .badge { padding: 6px 16px; border-radius: 999px; font-weight: 700; font-size: 0.88rem; display: inline-block; }
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

SAMPLE_EMAILS = {
    "🔴 Critical — Server Down Alert": """Hi Team,\n\nOur production server has been completely down for the past 2 hours.\nCustomers cannot access the platform and we are losing $5000 every hour.\nI need IMMEDIATE escalation to the CTO right now.\n\n- Ravi (Operations Head)""",
    "🟠 High — Job Offer Deadline": """Dear HR Team,\n\nI received your job offer letter yesterday and I am very interested.\nI need clarification on the salary structure before I sign.\nMy current employer needs a decision by this Friday EOD.\n\nBest regards,\nPriya Sharma""",
    "🟡 Medium — Project Status Update": """Hi Manager,\n\nI wanted to give you a quick update on the mobile app project.\nWe have completed the login module and are 60% done overall.\nThere are minor blockers with the API integration.\n\nThanks,\nArjun""",
    "🟢 Low — Team Lunch Invitation": """Hey everyone!\n\nJust a reminder that we are doing a team lunch this Friday at 1 PM.\nIt's completely optional but would love to see everyone there!\n\nCheers,\nSneha""",
    "🔴 Critical — Legal Notice": """To The Management,\n\nIf the pending payment of Rs.8,50,000 is not settled within 48 hours,\nwe will initiate legal proceedings immediately.\nThis is our final notice before court action.\n\nRegards,\nAdvocate Mehta""",
    "🟠 High — Client Escalation": """Dear Support Manager,\n\nMy subscription was charged twice in March and I still have not received\nthe refund despite 4 follow-up emails.\nIf not resolved by tomorrow, I will dispute the charge with my bank.\n\nKiran Reddy""",
    "🟡 Medium — Interview Reschedule": """Hi Recruiter,\n\nCould we please move the interview to Thursday or Friday?\nI have a prior medical appointment that I cannot reschedule.\n\nWarm regards,\nAditya Kumar""",
    "🟢 Low — Feedback Request": """Hi there,\n\nIf you have 2 minutes, please fill out our quick feedback form.\nYour opinion genuinely helps us improve.\nNo pressure at all!\n\nCustomer Success Team""",
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

st.title("📧 Email Intent & Urgency Detector")
st.markdown('<div class="subtitle">Paste any email — AI instantly detects <b>intent</b>, <b>urgency</b>, <b>sentiment</b> & <b>recommended action</b></div>', unsafe_allow_html=True)
st.divider()

st.subheader("💡 Try a Sample Email")
selected = st.selectbox("Choose a sample:", options=["-- Select a sample --"] + list(SAMPLE_EMAILS.keys()), label_visibility="collapsed")
sample_text = SAMPLE_EMAILS.get(selected, "") if selected != "-- Select a sample --" else ""

st.subheader("📩 Paste Your Email")
email_text = st.text_area(label="Email content", value=sample_text, height=220, placeholder="Dear Team,\n\nI wanted to follow up regarding...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔍 Analyze Email", type="primary", use_container_width=True):
    if not email_text.strip():
        st.error("⚠️ Please paste an email before clicking Analyze!")
    else:
        with st.spinner("🤖 AI is reading and analyzing your email..."):
            try:
                result = analyze_with_retry(email_text)

                st.markdown("<br>", unsafe_allow_html=True)
                st.success("✅ Analysis Complete!")
                st.divider()
                st.subheader("📊 Analysis Results")

                col1, col2, col3 = st.columns(3)
                col1.metric("🎯 Intent",    result.intent)
                col2.metric("⚡ Urgency",   result.urgency)
                col3.metric("😊 Sentiment", result.sentiment)

                st.markdown("<br>", unsafe_allow_html=True)

                urgency_badge   = URGENCY_BADGE.get(result.urgency, result.urgency)
                sentiment_badge = SENTIMENT_BADGE.get(result.sentiment, result.sentiment)
                st.markdown(f'<div class="badge-row">{urgency_badge}{sentiment_badge}</div>', unsafe_allow_html=True)

                st.divider()

                st.markdown("#### 📝 Email Summary")
                st.info(result.summary)

                st.markdown("#### ✅ Suggested Action")
                st.success(result.suggested_action)

                st.divider()

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
                elif "overloaded" in err.lower():
                    st.error("⚠️ LLM is overloaded. Please wait a minute and retry.")
                else:
                    st.error(f"❌ Error: {err}")
                    st.info("💡 Check your `.env` file has a valid `GROQ_API_KEY`")

st.divider()
st.markdown('<div class="footer">Built with ❤️ using LangChain + Groq LLaMA + Streamlit + Langfuse &nbsp;|&nbsp; Internship Project — Sprint 1</div>', unsafe_allow_html=True)
import streamlit as st
import os
import sys
import pandas as pd
import plotly.graph_objects as go
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from src.parser import parse_uploaded_file
from src.preprocess import clean_text
from src.matcher import rank_resumes, get_model
from src.skill_extractor import get_skill_gap
from src.ranker import rank_candidates

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="wide",
)

# ── CSS — works in BOTH light and dark mode ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── HERO BANNER ── */
.hero-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f2744 50%, #1a1a3e 100%);
    border-radius: 20px;
    padding: 3rem 2rem 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2.5rem;
    border: 1px solid rgba(102,126,234,0.3);
    box-shadow: 0 4px 32px rgba(102,126,234,0.15);
}
.main-header {
    font-size: 3.5rem;
    font-weight: 800;
    color: #00e5b0 !important;
    margin: 0 0 0.6rem 0;
    line-height: 1.1;
    letter-spacing: -1px;
    text-shadow: 0 0 40px rgba(0,229,176,0.4);
}
.sub-header {
    color: #93c5fd !important;
    font-size: 1.1rem;
    margin: 0;
    font-weight: 400;
}

/* ── SECTION HEADERS — visible in both themes ── */
.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: #6d28d9 !important;
    border-left: 5px solid #667eea;
    padding-left: 14px;
    margin: 1.5rem 0 1rem 0;
    line-height: 1.2;
}

/* ── SCORE CARDS — always white text on colored bg ── */
.score-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 14px;
    padding: 1.4rem;
    text-align: center;
    margin-bottom: 1rem;
}
.score-card h1 { font-size: 2.8rem; margin: 0; font-weight: 800; color: #ffffff !important; }
.score-card p  { margin: 4px 0 0 0; opacity: 0.95; font-size: 0.9rem; color: #ffffff !important; }
.rank-1 { background: linear-gradient(135deg, #f59e0b, #ef4444) !important; }
.rank-2 { background: linear-gradient(135deg, #6b7280, #9ca3af) !important; }
.rank-3 { background: linear-gradient(135deg, #92400e, #b45309) !important; }

/* ── SKILL BADGES — high contrast in both themes ── */
.skill-badge-match {
    display: inline-block;
    background: #059669;
    color: #ffffff !important;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 3px;
}
.skill-badge-miss {
    display: inline-block;
    background: #dc2626;
    color: #ffffff !important;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 3px;
}
.skill-badge-extra {
    display: inline-block;
    background: #2563eb;
    color: #ffffff !important;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 3px;
}

/* ── INFO BOX — adapts to both themes ── */
.info-box-light {
    background: #f0f4ff;
    border: 1px solid #c7d2fe;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.8rem;
    font-size: 0.92rem;
    color: #1e1b4b !important;
    line-height: 1.9;
}
.info-box-light strong { color: #4f46e5 !important; }

.info-box-dark {
    background: #1e2a3a;
    border: 1px solid #3b4f6b;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.8rem;
    font-size: 0.92rem;
    color: #e2e8f0 !important;
    line-height: 1.9;
}
.info-box-dark strong { color: #a78bfa !important; }

/* ── SCORE LABEL BADGES ── */
.badge-strong   { background:#059669; color:#fff !important; padding:3px 12px; border-radius:12px; font-size:12px; font-weight:700; }
.badge-moderate { background:#d97706; color:#fff !important; padding:3px 12px; border-radius:12px; font-size:12px; font-weight:700; }
.badge-weak     { background:#dc2626; color:#fff !important; padding:3px 12px; border-radius:12px; font-size:12px; font-weight:700; }

/* ── PRIMARY BUTTON ── */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: #ffffff !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding: 0.75rem 2rem !important;
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(102,126,234,0.35) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px rgba(102,126,234,0.55) !important;
}

/* ── METRIC CARDS ── */
[data-testid="metric-container"] {
    border-radius: 12px !important;
    padding: 1rem !important;
    border: 1px solid rgba(102,126,234,0.25) !important;
}

/* ── TABS ── */
[data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: #667eea !important;
    border-bottom: 3px solid #667eea !important;
}

/* ── SIDEBAR author text ── */
.author-tag {
    font-size: 0.85rem;
    color: #667eea !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1 class="main-header">🤖 AI Resume Screening System</h1>
    <p class="sub-header">Smart AI-Powered Candidate Ranking &amp; Resume Analysis Platform</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    st.markdown("### ⚙️ Settings")
    threshold = st.slider("Minimum match score (%)", 0, 100, 0, 5)
    top_n = st.number_input("Show top N candidates", 1, 50, 10)
    st.divider()
    st.markdown("##### 📊 Score Guide")
    st.markdown("🟢 **70–100%** → Strong match")
    st.markdown("🟡 **45–69%** → Moderate match")
    st.markdown("🔴 **0–44%** → Weak match")
    st.divider()
    st.markdown('<p class="author-tag">👨‍💻 Built by Ketan Rokade</p>', unsafe_allow_html=True)

# ── Input section ──────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<p class="section-header">📄 Upload Resumes</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX files",
        type=["pdf", "docx", "doc"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} resume(s) ready")
        for f in uploaded_files:
            st.caption(f"📎 {f.name}")

with col2:
    st.markdown('<p class="section-header">📋 Job Description</p>', unsafe_allow_html=True)
    jd_text = st.text_area(
        "Paste the Job Description here",
        height=240,
        placeholder="e.g. We are looking for a Python developer with experience in machine learning, NLP, Docker, and REST APIs...",
    )

st.divider()
run_btn = st.button("🚀 Screen Resumes Now", type="primary", use_container_width=True)

# ── Helper functions ───────────────────────────────────────────────────────────
def extract_contact_info(text):
    email    = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone    = re.findall(r'[\+\(]?[0-9][0-9\s\-\(\)]{7,}[0-9]', text)
    linkedin = re.findall(r'linkedin\.com/in/[\w\-]+', text, re.IGNORECASE)
    lines    = [l.strip() for l in text.strip().splitlines() if l.strip()]
    name     = lines[0] if lines else "Unknown"
    if '@' in name or 'http' in name.lower() or len(name) > 40:
        name = "Unknown"
    return {
        "name":     name,
        "email":    email[0] if email else "—",
        "phone":    phone[0].strip() if phone else "—",
        "linkedin": linkedin[0] if linkedin else "—",
    }

def extract_education(text):
    edu_keywords = ["b.tech","m.tech","btech","mtech","b.e","m.e",
                    "bachelor","master","mba","phd","b.sc","m.sc",
                    "bsc","msc","degree","university","college","institute"]
    for line in text.lower().splitlines():
        if any(k in line for k in edu_keywords):
            return line.strip().title()[:80]
    return "Not detected"

def extract_experience_years(text):
    matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience)?', text, re.IGNORECASE)
    return max((int(m) for m in matches), default=0)

def ats_score(text, jd):
    score = 0
    t = text.lower()
    if re.search(r'[\w\.-]+@[\w\.-]+', t): score += 15
    if re.search(r'[\+\(]?[0-9][0-9\s\-]{7,}', t): score += 10
    for kw in ["experience","education","skills","projects","summary"]:
        if kw in t: score += 5
    jd_words     = set(jd.lower().split())
    resume_words = set(t.split())
    overlap      = len(jd_words & resume_words)
    score       += min(int(overlap / max(len(jd_words), 1) * 30), 30)
    return min(score, 100)

# ── Processing ─────────────────────────────────────────────────────────────────
if run_btn:
    if not uploaded_files:
        st.error("❌ Please upload at least one resume.")
        st.stop()
    if not jd_text.strip():
        st.error("❌ Please paste a job description.")
        st.stop()

    with st.spinner("🔄 Loading AI model..."):
        get_model()

    candidate_names = []
    raw_texts       = []
    cleaned_texts   = []
    contact_infos   = []

    progress = st.progress(0, text="Parsing resumes...")
    for i, file in enumerate(uploaded_files):
        name = os.path.splitext(file.name)[0]
        candidate_names.append(name)
        raw = parse_uploaded_file(file)
        raw_texts.append(raw)
        cleaned_texts.append(clean_text(raw))
        contact_infos.append(extract_contact_info(raw))
        progress.progress((i + 1) / len(uploaded_files), text=f"📄 Parsed: {name}")
    progress.empty()

    with st.spinner("🧠 Computing AI similarity scores..."):
        jd_cleaned = clean_text(jd_text)
        scores     = rank_resumes(cleaned_texts, jd_cleaned)

    matched_list, missing_list, extra_list = [], [], []
    for raw in raw_texts:
        m, mi, e = get_skill_gap(raw, jd_text)
        matched_list.append(m)
        missing_list.append(mi)
        extra_list.append(e)

    ranked_df = rank_candidates(
        candidate_names, scores, matched_list, missing_list,
        threshold=threshold / 100.0
    )

    st.divider()
    st.markdown('<p class="section-header">📊 Screening Results</p>', unsafe_allow_html=True)

    if ranked_df.empty:
        st.warning(f"No candidates scored above {threshold}%. Lower the threshold.")
        st.stop()

    # ── Summary metrics ────────────────────────────────────────────────────────
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("📋 Total Resumes",    len(uploaded_files))
    m2.metric("✅ Candidates Shown", len(ranked_df))
    m3.metric("🏆 Top Score",        f"{ranked_df['Match Score (%)'].max()}%")
    m4.metric("📈 Avg Score",        f"{ranked_df['Match Score (%)'].mean():.1f}%")
    m5.metric("📉 Lowest Score",     f"{ranked_df['Match Score (%)'].min()}%")

    st.divider()

    tab1, tab2 = st.tabs(["🏆 Rankings", "📋 Full Report"])

    # ════════════════════════════════════════════════════════════════
    # TAB 1 — Rankings
    # ════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown("#### 🏆 Ranked Candidates")

        for _, row in ranked_df.head(int(top_n)).iterrows():
            rank  = int(row["Rank"])
            name  = row["Candidate"]
            score = float(row["Match Score (%)"])
            idx   = candidate_names.index(name)
            info  = contact_infos[idx]

            if score >= 70:
                badge_html = '<span class="badge-strong">🟢 Strong</span>'
            elif score >= 45:
                badge_html = '<span class="badge-moderate">🟡 Moderate</span>'
            else:
                badge_html = '<span class="badge-weak">🔴 Weak</span>'

            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"

            with st.expander(f"{medal}  {name}  —  {score}%", expanded=(rank <= 3)):

                # Score badge
                st.markdown(badge_html, unsafe_allow_html=True)
                st.write("")

                col_a, col_b, col_c = st.columns([1, 1, 2])

                with col_a:
                    rank_class = "rank-1" if rank==1 else "rank-2" if rank==2 else "rank-3" if rank==3 else ""
                    st.markdown(f"""
                    <div class="score-card {rank_class}">
                        <p>Match Score</p>
                        <h1>{score}%</h1>
                        <p>Rank #{rank}</p>
                    </div>""", unsafe_allow_html=True)

                with col_b:
                    matched = matched_list[idx]
                    missing = missing_list[idx]
                    extra   = extra_list[idx]
                    exp_yrs = extract_experience_years(raw_texts[idx])
                    ats     = ats_score(raw_texts[idx], jd_text)
                    st.metric("✅ Matched Skills", len(matched))
                    st.metric("❌ Missing Skills", len(missing))
                    st.metric("⭐ Bonus Skills",   len(extra))
                    st.metric("📅 Experience",     f"{exp_yrs} yrs" if exp_yrs else "N/A")
                    st.metric("🤖 ATS Score",      f"{ats}/100")

                with col_c:
                    # Donut — transparent bg so it works in both themes
                    fig = go.Figure(go.Pie(
                        labels=["Matched", "Missing"],
                        values=[max(len(matched), 0.01), max(len(missing), 0.01)],
                        hole=0.62,
                        marker_colors=["#059669", "#dc2626"],
                        textinfo="label+percent",
                        textfont_size=12,
                        textfont_color=["#ffffff", "#ffffff"],
                    ))
                    fig.update_layout(
                        height=210,
                        margin=dict(t=10, b=10, l=10, r=10),
                        showlegend=False,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Inter"),
                        annotations=[dict(
                            text=f"<b>{score}%</b>",
                            x=0.5, y=0.5,
                            font_size=20,
                            font_color="#667eea",
                            showarrow=False
                        )]
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Contact info box — uses st.info so it adapts to theme
                edu = extract_education(raw_texts[idx])
                st.info(
                    f"👤 **Name:** {info['name']}   |   "
                    f"📧 **Email:** {info['email']}   |   "
                    f"📞 **Phone:** {info['phone']}   |   "
                    f"🔗 **LinkedIn:** {info['linkedin']}   |   "
                    f"🎓 **Education:** {edu}"
                )

                # Skill badges
                st.markdown("**✅ Matched Skills:**")
                if matched:
                    st.markdown(
                        " ".join([f'<span class="skill-badge-match">{s}</span>' for s in matched]),
                        unsafe_allow_html=True
                    )
                else:
                    st.caption("None found")

                st.markdown("**❌ Missing Skills:**")
                if missing:
                    st.markdown(
                        " ".join([f'<span class="skill-badge-miss">{s}</span>' for s in missing]),
                        unsafe_allow_html=True
                    )
                else:
                    st.success("No missing skills — perfect match! ✅")

                if extra:
                    st.markdown("**⭐ Bonus Skills:**")
                    st.markdown(
                        " ".join([f'<span class="skill-badge-extra">{s}</span>' for s in extra]),
                        unsafe_allow_html=True
                    )

    # ════════════════════════════════════════════════════════════════
    # TAB 2 — Full Report
    # ════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown("#### 📋 Complete Candidate Report")

        report_rows = []
        for _, row in ranked_df.iterrows():
            name = row["Candidate"]
            idx  = candidate_names.index(name)
            info = contact_infos[idx]
            report_rows.append({
                "Rank":             row["Rank"],
                "Candidate":        name,
                "Email":            info["email"],
                "Phone":            info["phone"],
                "Match Score (%)":  row["Match Score (%)"],
                "ATS Score":        ats_score(raw_texts[idx], jd_text),
                "Experience (yrs)": extract_experience_years(raw_texts[idx]),
                "Matched Skills":   row["Matched Skills"],
                "Missing Skills":   row["Missing Skills"],
            })
        report_df = pd.DataFrame(report_rows)

        def color_score(val):
            if isinstance(val, (int, float)):
                if val >= 70:   return "color: #059669; font-weight: bold"
                elif val >= 45: return "color: #d97706; font-weight: bold"
                else:           return "color: #dc2626; font-weight: bold"
            return ""

        styled = report_df.style.map(color_score, subset=["Match Score (%)"])
        st.dataframe(styled, use_container_width=True, hide_index=True)

        csv = report_df.to_csv(index=False)
        st.download_button(
            "⬇️ Download Full Report as CSV",
            data=csv,
            file_name="resume_screening_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

else:
    st.info("👆 Upload resumes and paste a job description, then click **Screen Resumes Now** to begin.")

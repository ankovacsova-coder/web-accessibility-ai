import asyncio
import sqlite3
import json
import os
from datetime import datetime
import streamlit as st
from playwright.async_api import async_playwright
from axe_playwright_python.async_playwright import Axe
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. Professional UI Configuration
st.set_page_config(page_title="Accessibility Auditor", page_icon="🔍", layout="wide")

# Modern Theme-Aware CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [data-testid="stSidebar"] { font-family: 'Inter', sans-serif; }

    /* Hero Banner with Soft Pastel Gradient */
    .hero-banner {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 50%, #fff7ed 100%);
        padding: 60px;
        border-radius: 32px;
        margin-bottom: 40px;
        border: 1px solid rgba(0,0,0,0.05);
        color: #1e293b !important;
    }
    .hero-banner h1 {
        color: #1e293b !important;
        font-size: 52px !important;
        font-weight: 800 !important;
        margin-bottom: 15px !important;
        letter-spacing: -1.5px;
    }
    .hero-banner p {
        color: #475569 !important;
        font-size: 20px;
        max-width: 700px;
        line-height: 1.5;
    }

    /* Feature Badges - True Pastel Colors */
    .badge-container { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 30px; }
    .badge {
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 600;
        border: 1px solid transparent;
    }
    .badge-blue { background-color: #dbeafe; color: #1e40af; }
    .badge-orange { background-color: #ffedd5; color: #9a3412; }
    .badge-green { background-color: #dcfce7; color: #166534; }
    .badge-yellow { background-color: #fef9c3; color: #854d0e; }

    /* Sidebar & Buttons */
    [data-testid="stSidebar"] { border-right: 1px solid rgba(151, 166, 195, 0.2); }
    .stButton>button { border-radius: 12px !important; font-weight: 600 !important; }
    .stButton>button[kind="primary"] { background-color: #6366f1 !important; color: white !important; border: none !important; }

    /* AI Insight Box */
    .ai-insight {
        background-color: rgba(99, 102, 241, 0.03);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    st.markdown("### 🔍 Auditor")
    st.caption("Web Accessibility Analysis")
    st.divider()
    st.markdown("**TARGET URL**")
    target_url = st.text_input("URL", placeholder="example.com", key="url_input", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Run audit", type="primary", use_container_width=True):
            st.session_state["trigger_audit"] = True
    with c2:
        if st.button("Clear", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith("ai_res_") or key in ["display_results", "display_url"]:
                    del st.session_state[key]
            st.session_state["url_input"] = ""
            st.rerun()
    st.divider()
    st.markdown("**AUDIT HISTORY**")

# 3. Main Area - Hero Banner
st.markdown("""
    <div class="hero-banner">
        <h1>Build a web that everyone can use</h1>
        <p>Scan any page for WCAG 2.2 violations, explore issues by severity, and get AI-generated remediation guidance you can apply right away.</p>
        <div class="badge-container">
            <span class="badge badge-blue">🌐 Color contrast</span>
            <span class="badge badge-orange">⌨️ Keyboard nav</span>
            <span class="badge badge-green">🔊 Screen readers</span>
            <span class="badge badge-yellow">👁️ Visual clarity</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# 4. Database & Logic
def init_db():
    conn = sqlite3.connect("audits.db")
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS audits (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, violation_count INTEGER, full_results TEXT, timestamp DATETIME)')
    conn.commit()
    conn.close()


def save_audit(url, count, results_dict):
    conn = sqlite3.connect("audits.db")
    c = conn.cursor()
    json_results = json.dumps(results_dict)
    c.execute("INSERT INTO audits (url, violation_count, full_results, timestamp) VALUES (?, ?, ?, ?)",
              (url, count, json_results, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def get_history(limit=10):
    try:
        conn = sqlite3.connect("audits.db")
        c = conn.cursor()
        c.execute("SELECT id, url, violation_count, timestamp FROM audits ORDER BY timestamp DESC LIMIT ?", (limit,))
        data = c.fetchall()
        conn.close()
        return data
    except:
        return []


def load_audit_details(audit_id):
    conn = sqlite3.connect("audits.db")
    c = conn.cursor()
    c.execute("SELECT id, url, full_results FROM audits WHERE id = ?", (audit_id,))
    row = c.fetchone()
    conn.close()
    return (row[0], row[1], json.loads(row[2])) if row else (None, None, None)


init_db()


# 5. AI Logic
def get_ai_fix_suggestion(v_id, description, html_snippet):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        prompt = f"Act as a Senior Web Accessibility Consultant. Analyze violation: {v_id}. Description: {description}. Element: {html_snippet}. Provide User Impact, Business Risk, and Technical Fix with code."
        response = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}],
                                                  temperature=0.2)
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Analysis failed: {str(e)}"


# 6. Core Audit Logic
async def run_audit_logic(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            axe = Axe()
            results = await axe.run(page)
            return results.response
        except Exception as e:
            return None
        finally:
            await browser.close()


# 7. Main Logic Execution
if st.session_state.get("trigger_audit"):
    raw_url = st.session_state.url_input
    if raw_url:
        final_url = "https://" + raw_url.strip() if not raw_url.strip().startswith("http") else raw_url.strip()
        with st.spinner(f"Analyzing {final_url}..."):
            results = asyncio.run(run_audit_logic(final_url))
            if results:
                violations = results.get("violations", [])
                save_audit(final_url, len(violations), results)
                history = get_history(1)
                if history:
                    db_id, url, res = load_audit_details(history[0][0])
                    st.session_state["display_results"] = res
                    st.session_state["display_url"] = url
                    st.session_state["display_id"] = db_id
                st.session_state["trigger_audit"] = False
                st.rerun()

# 8. Results Display
if st.session_state.get("display_results"):
    res = st.session_state["display_results"]
    url = st.session_state["display_url"]
    audit_id = st.session_state.get("display_id")
    violations = res.get("violations", [])

    st.markdown(f"### Results for: `{url}`")
    st.metric("Total Violations Found", len(violations))

    for i, violation in enumerate(violations, 1):
        v_id = violation.get('id', 'unknown').upper()
        impact = violation.get('impact', 'unknown').upper()
        with st.expander(f"{i}. [{v_id}] - {impact}"):
            st.write(f"**Issue:** {violation['description']}")
            nodes = violation.get("nodes", [])
            if nodes:
                node = nodes[0]
                st.markdown("---")
                st.code(node.get("html"), language="html")
                ai_key = f"ai_res_{audit_id}_{v_id}"
                if st.button(f"✨ Generate AI Insight for {v_id}", key=f"btn_{ai_key}"):
                    with st.spinner("Analyzing..."):
                        st.session_state[ai_key] = get_ai_fix_suggestion(v_id, violation['description'],
                                                                         node.get("html"))
                if ai_key in st.session_state:
                    st.markdown(f'<div class="ai-insight">{st.session_state[ai_key]}</div>', unsafe_allow_html=True)

# Sidebar History
with st.sidebar:
    for a_id, h_url, h_count, h_time in get_history():
        short_url = h_url.replace("https://", "").replace("http://", "")[:20]
        if st.button(f"📄 {short_url} | {h_count} issues", key=f"hist_{a_id}", use_container_width=True):
            db_id, url, results = load_audit_details(a_id)
            st.session_state["display_results"] = results
            st.session_state["display_url"] = url
            st.session_state["display_id"] = db_id
            st.rerun()
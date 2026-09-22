import asyncio
import sqlite3
import json
import re
from datetime import datetime
import streamlit as st
from playwright.async_api import async_playwright
from axe_playwright_python.async_playwright import Axe

# 1. Professional UI Configuration
st.set_page_config(page_title="AI Accessibility Checker", page_icon="🐦‍⬛", layout="wide")

st.markdown("""
    <style>
    .stButton>button[kind="primary"] { background-color: #004a99; color: white; font-weight: bold; }
    .stButton>button[kind="secondary"] { text-align: left; width: 100%; color: #1a1a1a !important; background-color: #f0f2f6; border: 1px solid #d1d5db; }
    div[data-baseweb="input"] { border-color: transparent !important; }
    .stTextInput>div>div>input:focus { border-color: #004a99 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐦‍⬛ AI Accessibility Checker")


# 2. Database Logic
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
    # Prevent duplicates within 2 seconds
    c.execute("SELECT timestamp FROM audits WHERE url = ? ORDER BY timestamp DESC LIMIT 1", (url,))
    last = c.fetchone()
    if last:
        last_time = datetime.strptime(last[0], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_time).seconds < 2:
            conn.close()
            return
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
    c.execute("SELECT url, full_results FROM audits WHERE id = ?", (audit_id,))
    row = c.fetchone()
    conn.close()
    return (row[0], json.loads(row[1])) if row else (None, None)


init_db()

# 3. Session State Initialization
if "display_results" not in st.session_state:
    st.session_state["display_results"] = None
if "display_url" not in st.session_state:
    st.session_state["display_url"] = ""
if "trigger_audit" not in st.session_state:
    st.session_state["trigger_audit"] = False


# 4. Helper Functions & Callbacks
def handle_trigger():
    st.session_state["trigger_audit"] = True


def clear_all():
    st.session_state["url_input"] = ""
    st.session_state["display_results"] = None
    st.session_state["display_url"] = ""
    st.session_state["trigger_audit"] = False


def is_valid_url(url):
    """Basic validation to check if the input looks like a valid domain."""
    # Pattern: text + dot + at least 2 chars for TLD
    pattern = re.compile(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    clean_url = url.replace("https://", "").replace("http://", "").split('/')[0]
    return bool(pattern.match(clean_url))


def prepare_url(url):
    url = url.strip()
    if not url:
        return None
    if not is_valid_url(url):
        st.error(f"Invalid format: '{url}'. Please enter a valid domain (e.g., example.com).")
        return None
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


# 5. Core Audit Logic (Async)
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
            st.error(f"Audit failed: {e}")
            return None
        finally:
            await browser.close()


# 6. Sidebar
with st.sidebar:
    st.header("Audit Settings")
    st.text_input("Target URL:", placeholder="example.com", key="url_input", on_change=handle_trigger)

    col1, col2 = st.columns(2)
    with col1:
        st.button("Run Audit", type="primary", use_container_width=True, on_click=handle_trigger)
    with col2:
        st.button("Clear", use_container_width=True, on_click=clear_all)

    st.divider()
    st.header("Recent History")
    for a_id, h_url, h_count, h_time in get_history():
        if st.button(f"📄 {h_url}\n{h_time}", key=f"hist_{a_id}"):
            url, results = load_audit_details(a_id)
            st.session_state["display_results"] = results
            st.session_state["display_url"] = url
            st.session_state["trigger_audit"] = False

# 7. Main Area Logic
if st.session_state["trigger_audit"]:
    raw_url = st.session_state.url_input
    final_url = prepare_url(raw_url)

    if final_url:
        with st.spinner(f"Analyzing accessibility for {final_url}..."):
            results = asyncio.run(run_audit_logic(final_url))
            if results:
                violations = results.get("violations", [])
                save_audit(final_url, len(violations), results)
                st.session_state["display_results"] = results
                st.session_state["display_url"] = final_url
                st.session_state["trigger_audit"] = False
                st.rerun()
    st.session_state["trigger_audit"] = False

# Results Display
if st.session_state["display_results"]:
    res = st.session_state["display_results"]
    url = st.session_state["display_url"]
    violations = res.get("violations", [])

    st.success(f"Results for: {url}")
    st.metric("Total Violations", len(violations))

    for i, violation in enumerate(violations, 1):
        impact = violation.get('impact', 'unknown').upper()
        with st.expander(f"{i}. [{violation['id'].upper()}] - {impact}"):
            st.write(f"**Description:** {violation['description']}")
            for node in violation.get("nodes", []):
                st.code(node.get("html"), language="html")
                st.caption(f"Target: {' > '.join(node.get('target'))}")
else:
    if not st.session_state.url_input:
        st.info("👈 Enter a URL in the sidebar and press Enter or click 'Run Audit'.")
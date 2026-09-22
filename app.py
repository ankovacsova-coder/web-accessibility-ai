import asyncio
import sqlite3
import json
import os
import re
from datetime import datetime
import streamlit as st
from playwright.async_api import async_playwright
from axe_playwright_python.async_playwright import Axe
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (API Keys and Config)
load_dotenv()

# 1. Professional UI Configuration
st.set_page_config(page_title="AI Accessibility Checker", page_icon="🐦‍⬛", layout="wide")

st.markdown("""
    <style>
    .stButton>button[kind="primary"] { background-color: #004a99; color: white; font-weight: bold; }
    .stButton>button[kind="secondary"] { text-align: left; width: 100%; color: #1a1a1a !important; background-color: #f0f2f6; border: 1px solid #d1d5db; }
    div[data-baseweb="input"] { border-color: transparent !important; }
    .stTextInput>div>div>input:focus { border-color: #004a99 !important; }
    .ai-response { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #004a99; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐦‍⬛ AI Accessibility Checker")


# 2. Database Logic
def init_db():
    conn = sqlite3.connect("audits.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS audits
                 (
                     id
                     INTEGER
                     PRIMARY
                     KEY
                     AUTOINCREMENT,
                     url
                     TEXT,
                     violation_count
                     INTEGER,
                     full_results
                     TEXT,
                     timestamp
                     DATETIME
                 )''')
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
    c.execute("SELECT id, url, full_results FROM audits WHERE id = ?", (audit_id,))
    row = c.fetchone()
    conn.close()
    return (row[0], row[1], json.loads(row[2])) if row else (None, None, None)


init_db()


# 3. AI Logic (OpenAI Integration)
def get_ai_fix_suggestion(v_id, description, html_snippet):
    """Consults OpenAI to provide a human-readable fix for a specific violation."""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Use model from .env, default to gpt-4o-mini for cost efficiency
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        prompt = f"""
        Act as a Senior Web Accessibility Expert (WCAG 2.2).
        Analyze this technical violation and provide a clear fix:

        - Violation: {v_id}
        - Description: {description}
        - Broken HTML Snippet: {html_snippet}

        Provide your response in this structure:
        1. THE PROBLEM: Explain simply why this hurts users.
        2. THE FIX: Step-by-step instructions.
        3. CORRECTED CODE: The exact HTML code to use.

        Keep it professional and concise. Use Markdown.
        """

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Analysis failed: {str(e)}"


# 4. Session State & Callbacks
if "display_results" not in st.session_state:
    st.session_state["display_results"] = None
if "display_url" not in st.session_state:
    st.session_state["display_url"] = ""
if "display_id" not in st.session_state:
    st.session_state["display_id"] = None
if "trigger_audit" not in st.session_state:
    st.session_state["trigger_audit"] = False


def handle_trigger():
    st.session_state["trigger_audit"] = True


def clear_all():
    for key in list(st.session_state.keys()):
        if key.startswith("ai_res_") or key in ["display_results", "display_url", "display_id", "trigger_audit"]:
            del st.session_state[key]
    st.session_state["url_input"] = ""
    st.rerun()


def prepare_url(url):
    url = url.strip()
    if not url: return None
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
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
            db_id, url, results = load_audit_details(a_id)
            st.session_state["display_results"] = results
            st.session_state["display_url"] = url
            st.session_state["display_id"] = db_id
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
                # Reload to get the latest DB ID
                history = get_history(1)
                if history:
                    db_id, url, res = load_audit_details(history[0][0])
                    st.session_state["display_results"] = res
                    st.session_state["display_url"] = url
                    st.session_state["display_id"] = db_id
                st.session_state["trigger_audit"] = False
                st.rerun()
    st.session_state["trigger_audit"] = False

# Results Display
if st.session_state["display_results"]:
    res = st.session_state["display_results"]
    url = st.session_state["display_url"]
    audit_id = st.session_state["display_id"]
    violations = res.get("violations", [])

    st.success(f"Viewing results for: {url}")
    st.metric("Total Violations", len(violations))

    for i, violation in enumerate(violations, 1):
        v_id = violation.get('id', 'unknown').upper()
        impact = violation.get('impact', 'unknown').upper()

        with st.expander(f"{i}. [{v_id}] - {impact}"):
            st.write(f"**Description:** {violation['description']}")

            nodes = violation.get("nodes", [])
            if nodes:
                node = nodes[0]
                st.write("**Technical Details:**")
                st.code(node.get("html"), language="html")
                st.caption(f"Target: {' > '.join(node.get('target'))}")

                st.divider()

                # AI Analysis Section
                ai_storage_key = f"ai_res_{audit_id}_{v_id}"

                if st.button(f"✨ Get AI Fix for {v_id}", key=f"btn_{ai_storage_key}"):
                    with st.spinner("Consulting AI Expert..."):
                        suggestion = get_ai_fix_suggestion(v_id, violation['description'], node.get("html"))
                        st.session_state[ai_storage_key] = suggestion

                if ai_storage_key in st.session_state:
                    st.markdown('<div class="ai-response">', unsafe_allow_html=True)
                    st.markdown("### 🐦‍⬛ AI Expert Analysis")
                    st.markdown(st.session_state[ai_storage_key])
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    if not st.session_state.url_input:
        st.info("👈 Enter a URL in the sidebar and press Enter or click 'Run Audit'.")
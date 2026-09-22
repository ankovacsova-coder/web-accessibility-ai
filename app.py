import asyncio
import streamlit as st
from playwright.async_api import async_playwright
from axe_playwright_python.async_playwright import Axe

# 1. Professional UI Configuration
st.set_page_config(page_title="AI Accessibility Checker", page_icon="🐦‍⬛", layout="wide")

# Custom CSS to improve contrast and fix UI issues
st.markdown("""
    <style>
    /* 1. Improve contrast for primary buttons */
    .stButton>button[kind="primary"] {
        background-color: #004a99;
        color: white;
        border: 1px solid white;
        font-weight: bold;
    }

    /* 2. KILL THE RED BORDER on text input */
    /* This targets the input field when it's focused or active */
    .stTextInput>div>div>input:focus {
        border-color: #004a99 !important;
        box-shadow: 0 0 0 0.2rem rgba(0, 74, 153, 0.25) !important;
    }

    /* This targets the container to prevent the red glow */
    .st-emotion-cache-163npsa:focus-within {
        border-color: #004a99 !important;
    }

    /* General fix for the red ghost border */
    div[data-baseweb="input"] {
        border-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🐦‍⬛ AI Accessibility Checker")

# Initialize session state for triggering the audit
if "run_audit" not in st.session_state:
    st.session_state["run_audit"] = False


# 2. Helper function to ensure URL has a protocol
def prepare_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


# 3. Callback functions for UI controls
def trigger_audit():
    st.session_state["run_audit"] = True


def clear_all():
    st.session_state["url_input"] = ""
    st.session_state["run_audit"] = False


# 4. Core Audit Logic (Async)
async def run_audit(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            axe = Axe()
            results = await axe.run(page)
            return results.response
        except Exception as e:
            st.error(f"Error during audit: {e}")
            return None
        finally:
            await browser.close()


# 5. Sidebar for Input and Controls
with st.sidebar:
    st.header("Audit Settings")

    # on_change triggers when user hits Enter
    target_url = st.text_input(
        "Target URL:",
        placeholder="example.com",
        key="url_input",
        on_change=trigger_audit
    )

    col1, col2 = st.columns(2)
    with col1:
        # on_click triggers when user clicks the button
        st.button("Run Audit", type="primary", use_container_width=True, on_click=trigger_audit)
    with col2:
        st.button("Clear", use_container_width=True, on_click=clear_all)

    st.divider()
    st.caption("Powered by Axe-core & Playwright")

# 6. Main Area Execution Logic
if st.session_state["run_audit"]:
    if target_url:
        final_url = prepare_url(target_url)
        with st.spinner(f"Performing accessibility audit for {final_url}..."):
            results = asyncio.run(run_audit(final_url))

            if results:
                violations = results.get("violations", [])
                st.success(f"Audit complete for {final_url}. Found {len(violations)} violations.")

                for i, violation in enumerate(violations, 1):
                    impact = violation.get('impact', 'unknown').upper()
                    with st.expander(f"{i}. [{violation['id'].upper()}] - {impact}"):
                        st.write(f"**Description:** {violation['description']}")
                        st.write("**Affected Elements:**")
                        for node in violation.get("nodes", []):
                            st.code(node.get("html"), language="html")
                            st.caption(f"Target: {' > '.join(node.get('target'))}")

        # Reset the trigger so it doesn't run again on next interaction
        st.session_state["run_audit"] = False
    else:
        st.warning("Please enter a URL in the sidebar to start the audit.")
        st.session_state["run_audit"] = False
else:
    if not target_url:
        st.info("👈 Enter a URL in the sidebar and click 'Run Audit' or press Enter to begin.")
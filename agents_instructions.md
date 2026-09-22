# Project Blueprint: AI-Native Accessibility Checker

## Project Overview
Build a professional web accessibility auditing platform using Python, Streamlit, and Playwright. The tool must perform deep DOM analysis using Axe-core and maintain a persistent history of audits in a local SQLite database.

## Technical Stack
- **Language:** Python 3.12+
- **Browser Automation:** Playwright (Chromium)
- **A11y Engine:** `axe-playwright-python`
- **Frontend:** Streamlit (Wide layout)
- **Database:** SQLite
- **Security:** `python-dotenv` for API keys

## Core Logic Requirements

### 1. URL Validation & Preparation
- Implement a regex-based validation to ensure the input is a valid domain (e.g., `example.com`).
- Automatically prepend `https://` if the protocol is missing.
- Strip leading/trailing whitespace from user input.

### 2. Asynchronous Audit Engine
- Use `async_playwright` to launch a headless Chromium browser.
- Navigate to the target URL with `wait_until="networkidle"` and a 60s timeout.
- Execute Axe audit and extract the `.response` attribute from the results object.
- **Data Extraction:** For each violation, extract:
    - `id` and `description`
    - `impact` level (Critical, Serious, Moderate, Minor)
    - `nodes`: For each node, get the `html` snippet and the `target` (CSS selector path).

### 3. Data Persistence (SQLite)
- **Initialization:** Use `CREATE TABLE IF NOT EXISTS` to ensure the DB file (`audits.db`) is created on first run.
- **Schema:** Store `id`, `url`, `violation_count`, `full_results` (as a JSON string/TEXT), and `timestamp`.
- **Duplicate Prevention:** Before saving, check if the same URL was audited within the last 2 seconds to prevent double-entries during Streamlit reruns.
- **Retrieval:** Implement a function to load full JSON details by `audit_id`.

## UI & UX Specifications (Streamlit)

### 1. Layout & Styling
- Set `layout="wide"` in `st.set_page_config`.
- **Sidebar:** Use for inputs (URL, Run, Clear) and History list.
- **Main Area:** Reserved for audit results and spinners.
- **Custom CSS:**
    - Improve contrast for primary buttons (Deep Blue: `#004a99`).
    - Remove the default Streamlit red focus border on text inputs using `!important` CSS overrides.
    - Ensure high contrast for history buttons in the sidebar.

### 2. State & Event Handling (Crucial)
- **Avoid `st.form`:** It causes visual glitches (red borders) and overlapping text in narrow sidebars.
- **Triggers:** Use `st.session_state` to manage audit triggers.
- **Callbacks:** Use `on_change` for the text input and `on_click` for buttons to trigger the audit logic. This ensures the **Enter key** and **Button click** work reliably.
- **Reruns:** Call `st.rerun()` immediately after saving a new audit to the database to refresh the sidebar history.

### 3. Results Display
- Use `st.metric` for the total violation count.
- Use `st.expander` for each violation type.
- Inside expanders, use `st.code(language="html")` for HTML snippets and `st.caption` for CSS targets.

## Security & Project Structure
- Exclude `.env` and `audits.db` from version control via `.gitignore`.
- Provide a `requirements.txt` with pinned versions for reproducibility.
- Include a `README.md` documenting known framework limitations (e.g., Streamlit's internal a11y issues).
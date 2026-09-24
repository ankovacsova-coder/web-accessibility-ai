# Project Blueprint: Professional AI Accessibility Checker

## Project Goal

Create a professional web accessibility auditing platform that translates technical WCAG violations into human-readable business risks and technical solutions.

## Technical Specifications

- **Core:** Python 3.12+, Playwright (Async), Axe-core (`axe-playwright-python`).
- **UI:** Streamlit (Wide layout, Inter font, SaaS Blue theme: `#2563eb`).
- **Data:** SQLite for persistent storage of full JSON audit results.
- **AI:** OpenAI API integration using a model-agnostic approach via `.env`.

## Logic Requirements

### 1. Robust URL Handling

- Validate input using regex (domain format).
- Auto-prepend `https://` and strip whitespace.
- Prevent redundant audits via a 2-second duplicate check in the database.

### 2. Database Schema

- **Table:** `audits`
- **Columns:** `id` (PK), `url`, `violation_count`, `full_results` (TEXT/JSON), `timestamp`.
- **Requirement:** Must store the *entire* Axe-core response for future AI re-analysis.

### 3. AI Prompt Engineering (Crucial)

- **Role:** Senior Web Accessibility Consultant & Business Analyst.
- **Input:** Violation ID, Description, and HTML Snippet.
- **Output Structure:**
  1. **USER EXPERIENCE IMPACT:** Non-technical, empathetic explanation of the barrier.
  2. **BUSINESS & LEGAL RISK:** Mention of EAA 2025 compliance and business loss.
  3. **TECHNICAL REMEDIATION:** Step-by-step fix + corrected HTML code block.
- **Implementation:** Use `st.session_state` to cache AI responses per `audit_id` and `violation_id`.

## UI/UX Requirements

- **Sidebar:** Audit Settings (Input, Run, Clear) and a clickable Audit History list.
- **Main Area:** Success/Error messages, Total Violations metric, and Expandable violation details.
- **Styling:**
  - Use `st.markdown` with custom CSS to inject the 'Inter' font.
  - Style primary buttons with modern blue (`#2563eb`).
  - Style AI response boxes with white background, borders, and subtle shadows.
  - Ensure all history buttons are high-contrast and accessible.
- **Stability:** Use `on_change` and `on_click` callbacks to manage the `trigger_audit` state. Ensure the spinner appears in the main area.

## Security & Maintenance

- Exclude `audits.db` and `.env` from Git.
- Maintain a pinned `requirements.txt`.
- Document framework limitations regarding accessibility in the README.

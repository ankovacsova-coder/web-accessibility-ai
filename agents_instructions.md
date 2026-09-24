# Project Blueprint: AI Accessibility Checker

## Purpose

Build a Streamlit-based web accessibility auditing application that scans public web pages, stores results locally, and optionally generates AI-based accessibility explanations and remediation guidance.

This document is intended to help an AI system recreate the application with minimal additional prompting. It should define the app’s required architecture, behavior, UI, data flow, and testing expectations.

---

## Product Summary

The app is a single-page accessibility audit tool with these responsibilities:

1. accept a user-provided URL or domain
2. open the page in a headless Chromium browser
3. run an accessibility audit using axe-core
4. store the full result locally in SQLite
5. display violations in a clean UI
6. generate AI insights for individual violations on demand
7. allow previous audits to be reopened from history

---

## Required Tech Stack

- **Language:** Python 3.12+
- **UI:** Streamlit
- **Browser Automation:** Playwright (Python)
- **Accessibility Engine:** `axe-playwright-python`
- **AI:** OpenAI Python SDK
- **Persistence:** SQLite
- **Config:** `python-dotenv`

---

## Required Files

The generated project should include at minimum:

```text
web-accessibility-ai/
├── app.py
├── requirements.txt
├── README.md
├── agents_instructions.md
└── tests/
    ├── conftest.py
    ├── test_ui.py
    └── test_functionality.py
```

Optional:
- `.env.example`
- `.gitignore`

---

## Core Functional Requirements

### 1. URL Input
The UI must provide a sidebar text input for a URL or domain.

Requirements:
- input key must be `url_input`
- placeholder should be `example.com`
- whitespace must be stripped before use
- if the value does not start with `http://` or `https://`, prepend `https://`

### 2. Run Audit Action
The UI must include a **Run audit** button.

When clicked:
- set a session-state trigger
- execute the audit
- show a spinner while processing
- display results in the main content area
- save the results to SQLite

### 3. Clear Action
The UI must include a **Clear** button.

When clicked:
- clear the current input
- clear current displayed results
- clear cached AI responses from `st.session_state`
- preserve the historical database records

### 4. Audit History
The sidebar must include a clickable list of previous audits.

History item behavior:
- show shortened URL + issue count
- clicking a history item reloads the stored result from SQLite
- no new browser scan should be run when reopening history

### 5. Accessibility Scan
The app must:
- launch Chromium headlessly using Playwright
- navigate to the target page
- wait for page readiness
- run axe-core through `axe-playwright-python`
- capture and return the full audit response

### 6. AI Insight Generation
Each displayed violation should include an action to generate AI guidance.

Input to the AI prompt:
- violation ID
- violation description
- sample HTML snippet

Expected AI output structure:
1. user experience impact
2. business and legal risk
3. technical remediation
4. corrected code example when appropriate

AI responses should be cached in `st.session_state` using a stable key derived from:
- audit ID
- violation ID

---

## Database Requirements

Use SQLite with a table named `audits`.

Required schema:

- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `url` TEXT
- `violation_count` INTEGER
- `full_results` TEXT
- `timestamp` DATETIME

Rules:
- store the entire axe-core response in `full_results`
- use JSON serialization for storage
- order history by most recent timestamp first

---

## UI / UX Requirements

### Sidebar
Must contain:
- app heading
- short caption
- URL input
- Run audit button
- Clear button
- Audit history list

### Main Area
Must contain:
- hero/banner section
- scan results summary
- total violations metric
- expandable violation rows
- code snippet preview for affected HTML
- optional AI insight box

### Style Requirements
- use Streamlit wide layout
- inject the Inter font via CSS
- use a modern, clean SaaS-like visual style
- buttons should be high contrast and readable
- AI insight container should be visually separated
- overall layout should remain simple and professional

---

## State Management Requirements

Use `st.session_state` for:
- `url_input`
- `trigger_audit`
- `display_results`
- `display_url`
- `display_id`
- cached AI outputs such as `ai_res_<audit_id>_<violation_id>`

The app should avoid unnecessary reruns where possible, but Streamlit reruns are acceptable as part of normal interaction flow.

---

## Error Handling Requirements

The app should handle these cases gracefully:
- empty input
- page load failure
- Playwright/browser failure
- axe scan failure
- invalid or blocked target URL
- AI API error

Preferred behavior:
- do not crash
- return `None` or show a user-friendly warning/error
- keep the app usable after failure

---

## Testing Requirements

Provide Playwright-based pytest tests.

### Required tests

#### `tests/test_ui.py`
Should verify:
- app loads successfully
- page title is correct
- main hero heading is visible
- sidebar is visible
- URL input is visible
- Run audit button is visible
- Clear button is visible

#### `tests/test_functionality.py`
Should verify:
- Clear button resets the input field
- entering a URL and running an audit displays a result section

#### `tests/conftest.py`
Should:
- start Streamlit automatically for the test session
- wait until the app is reachable on `http://localhost:8501`
- terminate the process after tests finish

Use `sys.executable -m streamlit run app.py` rather than relying on a global `streamlit` command.

---

## Environment Variables

The app should read from `.env`.

Required:
- `OPENAI_API_KEY`

Optional:
- `OPENAI_MODEL` with default `gpt-4o-mini`

---

## Security and Privacy Requirements

- do not commit `.env`
- do not commit `audits.db`
- explain local storage behavior in `README.md`
- avoid exposing API keys in code
- treat stored audit results as potentially sensitive

---

## Known Framework Limitations

The implementation uses Streamlit, which may introduce accessibility issues in framework-rendered markup that are outside direct control of the Python code.

The generated README should mention:
- possible framework ARIA issues
- possible landmark/region issues
- possible contrast issues in default widgets

---

## Non-Goals

The app does not need to support:
- authentication flows
- multi-page crawling
- report export
- batch audits
- distributed processing
- real-time collaboration

These may be future enhancements but are not required for the baseline version.

---

## Acceptance Criteria

A generated version of the app is acceptable only if it satisfies all of the following:

1. `app.py` launches with `streamlit run app.py`
2. the sidebar includes URL input, Run audit, Clear, and Audit History
3. entering `example.com` results in scanning `https://example.com`
4. audits are stored in SQLite and can be reopened from history
5. violation details are displayed in expandable sections
6. AI insight generation works when an API key is configured
7. the project includes a useful `README.md`
8. the project includes Playwright pytest tests
9. tests are aligned with the actual rendered UI
10. dependencies are pinned in `requirements.txt`

---

## Implementation Guidance for AI Generators

When generating the app:
- prefer readable, single-file implementation for `app.py`
- keep helper functions small and explicit
- avoid unnecessary abstractions
- use stable widget labels and keys so tests remain reliable
- ensure the final code is consistent with the README and tests
- do not document features that are not actually implemented

---

## Important Consistency Rule

The following must always remain aligned:
- widget labels in `app.py`
- selectors used in tests
- workflow described in `README.md`

If any UI label or input behavior changes, update all three.
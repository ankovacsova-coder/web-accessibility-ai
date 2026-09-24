# AI Accessibility Checker 🔍

A Streamlit-based web accessibility auditing application powered by **Playwright**, **axe-core**, and **OpenAI**.

This tool scans public web pages for accessibility issues, stores audit history locally, and optionally generates AI-assisted explanations and remediation guidance for each violation.

---

## Overview

The application is designed to help developers, QA engineers, accessibility specialists, and product teams:

- run accessibility audits against live websites
- review violations grouped by severity and rule ID
- understand accessibility issues in both technical and business terms
- store historical audit results locally for later review
- generate AI explanations and remediation suggestions for specific issues

The app combines:

- **Playwright** for browser automation
- **axe-core** via `axe-playwright-python` for accessibility analysis
- **Streamlit** for the user interface
- **SQLite** for local audit history
- **OpenAI** for AI-generated issue explanations and remediation guidance

---

## Main Features

- **Accessibility scanning of live web pages**
- **Automatic HTTPS prefixing** for domains entered without protocol
- **Persistent audit history** stored in a local SQLite database
- **Expandable issue details** for each violation
- **AI-generated explanations** for:
  - user impact
  - business and legal risk
  - technical remediation suggestions
- **Simple operator workflow** through a sidebar-based interface

---

## How the Application Works

### 1. Enter a URL
The user types a domain or URL in the sidebar input field.

Examples:

- `example.com`
- `https://example.com`
- `https://www.w3.org/WAI/`

If the input does not start with `http://` or `https://`, the app automatically prefixes it with `https://`.

### 2. Run the audit
When the user clicks **Run audit**, the app:

1. launches a headless Chromium browser using Playwright
2. opens the target page
3. runs an accessibility scan using axe-core
4. collects the results
5. stores the full JSON response in SQLite
6. displays a summary and detailed violations in the UI

### 3. Review the results
For each violation, the app shows:

- rule ID
- impact level
- human-readable issue description
- one example HTML node from the page

### 4. Generate AI insights
For each violation, the user can click **Generate AI Insight**.

The app sends the following to the OpenAI API:

- violation ID
- violation description
- related HTML snippet

The AI response is expected to provide:

1. **User Experience Impact**
2. **Business & Legal Risk**
3. **Technical Remediation**

### 5. Reopen previous audits
Past audits are listed in the sidebar under **Audit History**.

Clicking a history item reloads the stored result from `audits.db` without re-running the scan.

---

## Tech Stack

- **Python** 3.12+
- **Streamlit**
- **Playwright**
- **axe-playwright-python**
- **OpenAI Python SDK**
- **SQLite**
- **python-dotenv**

---

## Project Structure

```text
web-accessibility-ai/
├── app.py
├── requirements.txt
├── README.md
├── agents_instructions.md
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   ├── conftest.py
│   ├── test_ui.py
│   └── test_functionality.py
└── audits.db
```

---

## Installation

### 1. Clone the repository

```powershell
git clone <your-repository-url>
cd web-accessibility-ai
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Playwright browser binaries

```powershell
python -m playwright install chromium
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

### Variables

- `OPENAI_API_KEY`  
  Required only if you want AI-generated insights.

- `OPENAI_MODEL`  
  Optional. Defaults to `gpt-4o-mini` if not set.

> Important: `.env` files must use standard `KEY=value` syntax.  
> Do **not** use GitHub Actions expressions such as `${{ secrets.OPENAI_API_KEY }}` inside `.env`.  
> That syntax belongs only in GitHub Actions workflow YAML files.

---

## Running the Application

Start the Streamlit app:

```powershell
streamlit run app.py
```

Then open the local URL shown in the terminal, typically:

```text
http://localhost:8501
```

---

## Usage Guide

### Run an accessibility audit
1. Launch the app
2. Enter a domain or full URL in the sidebar
3. Click **Run audit**
4. Wait for the scan to complete
5. Review the total number of violations and issue details

### Clear current state
Click **Clear** to reset:
- current input
- current displayed results
- cached AI outputs in session state

### Reopen previous results
Use the **Audit History** section in the sidebar to reload a previous scan.

### Generate AI remediation help
Expand a violation and click **Generate AI Insight**.

---

## Local Data Storage

The app stores audit results in a local SQLite database:

- file: `audits.db`
- table: `audits`

Stored fields include:
- `id`
- `url`
- `violation_count`
- `full_results`
- `timestamp`

The `full_results` field stores the entire axe-core response as JSON text so that results can be reloaded later without rescanning.

---

## Testing

The project includes Playwright-based UI tests under `tests/`.

### Run tests

```powershell
pytest -q
```

### Notes about tests

- Tests start the Streamlit app automatically through `tests/conftest.py`
- Tests require Playwright and Chromium to be installed
- Tests are end-to-end UI tests, so they depend on the rendered Streamlit interface
- Tests may be slower when a real external website is audited
- Tests that depend on live websites may be more fragile because of network variability or anti-bot protections

---

## Continuous Integration

This project can be tested automatically with GitHub Actions.

A typical CI workflow should:
- install Python dependencies
- install Playwright browser binaries
- run pytest

When using GitHub Actions, pass secrets through workflow environment variables, for example:

```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  OPENAI_MODEL: gpt-4o-mini
```

Do not commit real secrets to the repository and do not place GitHub Actions secret expressions inside `.env`.

---

## Troubleshooting

### Playwright browser is missing
If you see errors about missing browser binaries:

```powershell
python -m playwright install chromium
```

### AI insight generation fails
Check:
- `.env` exists
- `OPENAI_API_KEY` is valid
- internet access is available
- the selected model name is valid for your OpenAI account

### Audit does not return results
Possible causes:
- target site blocks automation
- page takes too long to load
- the site requires login
- transient browser/network errors occurred

### Tests fail because elements are missing
The test selectors must match the actual Streamlit UI. If `app.py` changes, the tests may need to be updated as well.

---

## Known Limitations

### Streamlit-generated accessibility limitations
Because the app uses Streamlit, some accessibility issues can come from Streamlit-generated markup rather than your custom Python code.

Examples may include:
- ARIA attribute issues in framework-rendered controls
- imperfect landmark structure
- framework-level contrast issues in default widgets

### External site variability
Live scans depend on:
- network availability
- target page stability
- page load time
- anti-bot protections

### Current audit scope
The app audits a loaded page in a headless Chromium session. It does not currently:
- crawl multiple pages
- authenticate into protected apps
- compare audits over time
- export reports
- support batch processing

---

## Security and Privacy

- `.env` should never be committed to Git
- `audits.db` may contain sensitive audit history and should not be committed
- AI prompts may include HTML snippets from audited pages
- use caution when auditing pages containing sensitive content
- `.env` must use standard dotenv syntax: `KEY=value`
- GitHub Actions secret expressions must only be used in workflow YAML files

---

## Suggested Future Improvements

- stronger URL validation
- duplicate-audit suppression
- export to JSON/CSV/PDF
- multi-page crawling
- issue filtering by severity
- authentication support
- background job processing
- report comparison between historical runs

---

## Development Notes

The current implementation centers around:

- `run_audit_logic()` in `app.py` for Playwright + axe execution
- `save_audit()`, `get_history()`, and `load_audit_details()` for local persistence
- `get_ai_fix_suggestion()` for AI-generated issue analysis
- `st.session_state` for UI state and temporary AI result caching

---

## License / Usage

Add your preferred license and usage terms here.
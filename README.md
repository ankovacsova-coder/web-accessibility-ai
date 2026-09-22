AI Accessibility Checker 🐦‍⬛
A professional, high-performance web accessibility auditing platform powered by Playwright, Axe-core, and SQLite. This application provides deep technical insights into WCAG compliance and maintains a persistent history of audits for long-term quality tracking.

🚀 Key Features
Automated Deep Scanning: Utilizes the industry-standard Axe-core engine to perform comprehensive DOM analysis.
Persistent History: Integrated SQLite database to store and retrieve full audit results (JSON) for historical comparison.
Interactive Dashboard: A modern, wide-layout UI built with Streamlit, featuring a dedicated sidebar for controls and history management.
Technical Precision: Detailed violation reports including:
Impact levels (Critical, Serious, Moderate, Minor).
Exact CSS selector paths (Targets).
Syntax-highlighted HTML snippets of affected elements.
Smart URL Validation: Built-in regex validation to ensure correct domain formatting and automatic protocol handling (HTTPS).
AI-Native Ready: Data structure optimized for Phase 3: AI-driven remediation and automated code fixing.
🛠️ Tech Stack
Language: Python 3.12+
Browser Automation: Playwright
Accessibility Engine: Axe-core (via axe-playwright-python)
Database: SQLite (Local persistence)
Frontend: Streamlit
Environment Management: python-dotenv
📦 Installation
Clone the repository:

git clone <your-repository-url>
cd web-accessibility-ai
Set up a virtual environment:

python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Install Playwright browsers:

playwright install chromium
🖥️ Usage
Run the application:
streamlit run app.py
Perform an Audit: Enter a domain (e.g., example.com) in the sidebar and press Enter or click "Run Audit".
Browse History: Click on any previous audit in the "Recent History" sidebar to instantly reload and view its detailed results.
Clear State: Use the "Clear" button to reset the UI and input fields.
💾 Database & Persistence
The application automatically initializes a local SQLite database (audits.db) upon first launch.

Full Results: Unlike basic tools, this platform stores the entire JSON response from the audit engine, ensuring no data is lost for future analysis.
Privacy: The database file is excluded from version control via .gitignore to protect private audit data.
🔍 Accessibility Audit of this Tool
This tool has been audited using its own engine to ensure transparency.

Known Issues: As a prototype built on the Streamlit framework, certain framework-level violations (ARIA roles in sidebar, region landmarks) are documented.
Strategic Resolution: For production environments, a migration to a custom frontend implementation (e.g., a dedicated web framework) is planned to ensure 100% WCAG 2.2 compliance.
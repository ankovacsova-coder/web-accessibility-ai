AI Accessibility Checker 🐦‍⬛
A professional web accessibility auditing tool powered by Playwright, Axe-core, and AI. This application scans websites for WCAG compliance violations and provides technical insights for developers.

🚀 Features
Automated Scanning: Deep DOM analysis using the industry-standard Axe-core engine.
Technical Insights: Detailed reports including impact levels, CSS selectors (targets), and HTML snippets.
Interactive UI: A clean, web-based dashboard built with Streamlit.
AI-Native Ready: Structured data output prepared for AI-driven remediation (Phase 3).
🛠️ Tech Stack
Language: Python 3.12+
Browser Automation: Playwright
Accessibility Engine: Axe-core (via axe-playwright-python)
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
Access the dashboard: Open your browser at http://localhost:8501.
Perform an audit: Enter a target URL and click "Run Audit".
🔒 Security
API keys and private configurations are stored in a .env file.
The .env file is excluded from version control via .gitignore.
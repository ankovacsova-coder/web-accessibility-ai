AI Accessibility Checker 🐦‍⬛
A professional, high-performance web accessibility auditing platform powered by Playwright, Axe-core, and OpenAI. This application provides deep technical insights into WCAG compliance and utilizes AI to provide human-readable remediation advice and code fixes.

🚀 Key Features
Automated Deep Scanning: Comprehensive DOM analysis using the industry-standard Axe-core engine.
AI-Powered Remediation: Integrated OpenAI GPT-4o analysis for every violation, providing:
Human-readable explanations of the impact.
Step-by-step fix instructions.
Corrected HTML code snippets ready for implementation.
Persistent History: Integrated SQLite database to store and retrieve full audit results (JSON) for historical tracking.
Interactive Dashboard: A modern, wide-layout UI built with Streamlit, featuring a dedicated sidebar for controls and history management.
Smart URL Validation: Built-in regex validation and automatic HTTPS protocol handling.
🛠️ Tech Stack
Language: Python 3.12+
Browser Automation: Playwright
Accessibility Engine: Axe-core
AI Integration: OpenAI API (GPT-4o)
Database: SQLite
Frontend: Streamlit
📦 Installation
Clone the repository:

git clone <your-repository-url>
cd web-accessibility-ai
Set up a virtual environment:

python -m venv .venv
.venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Configure Environment Variables: Create a .env file in the root directory and add your OpenAI API key:

OPENAI_API_KEY=your_sk_key_here
Install Playwright browsers:

playwright install chromium
🖥️ Usage
Run the application:
streamlit run app.py
Perform an Audit: Enter a domain in the sidebar and click "Run Audit".
Get AI Assistance: Expand any violation in the results and click "✨ Get AI Fix" to receive expert remediation advice.
Browse History: Click on any previous audit in the sidebar to instantly reload past results.
💾 Database & Privacy
Full audit results are stored locally in audits.db.
The database and .env files are excluded from version control to ensure data privacy and security.
🔍 Accessibility Audit of this Tool
This tool has been audited using its own engine. Framework-level limitations (Streamlit) are documented in the code, with a strategic roadmap for migration to a custom frontend for 100% WCAG 2.2 compliance in production.
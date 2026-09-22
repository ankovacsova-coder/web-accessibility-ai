AI Accessibility Checker 🐦‍⬛

A professional web accessibility auditing tool powered by Playwright, Axe-core, and AI. 
This application scans websites for WCAG compliance violations and provides technical insights for developers.

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

🔍 Accessibility Audit of this Tool
To demonstrate the integrity of this project, the AI Accessibility Checker has been audited using its own engine. The following findings represent the current state of the Streamlit-based prototype:

Known Issues (Framework Related)
As this tool is a prototype built on the Streamlit framework, certain accessibility violations are present in the generated HTML structure that cannot be directly modified within the Python layer:

[ARIA-ALLOWED-ATTR] (Critical): The framework applies aria-expanded to <section> elements (sidebar), which is technically non-compliant with standard ARIA roles.
[COLOR-CONTRAST] (Serious): Certain default Streamlit components (e.g., info banners, footer links) do not meet the WCAG AA minimum contrast ratio.
[REGION] (Moderate): Some framework-generated containers are not wrapped in appropriate HTML5 landmarks (e.g., main, nav).

Strategic Resolution
In a production environment, these issues would be resolved by:

Custom Frontend Implementation: Migrating from a rapid prototyping framework to a production-ready frontend solution (e.g., a dedicated web framework or a custom-built UI) that allows full control over semantic HTML and ARIA attributes.
Accessible Design System: Implementing a verified design system with color palettes that strictly adhere to WCAG contrast requirements.
Semantic Structure: Ensuring all page regions are correctly identified using standard HTML5 landmarks and appropriate ARIA roles.
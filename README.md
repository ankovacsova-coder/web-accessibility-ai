# AI Accessibility Checker 🔍

A professional, high-performance web accessibility auditing platform powered by **Playwright**, **Axe-core**, and **OpenAI**. This application provides deep technical insights into WCAG 2.2 compliance and utilizes AI to bridge the gap between technical violations and business impact.

## 🚀 Key Features

- **Automated Deep Scanning:** Comprehensive DOM analysis using the industry-standard Axe-core engine.
- **Dual-Audience AI Insights:** Integrated **GPT-4o** analysis that provides:
  - 👤 **User Experience Impact:** Empathetic, non-technical explanations of how errors affect people with disabilities.
  - 💼 **Business & Legal Risk:** Analysis of compliance risks (e.g., European Accessibility Act 2025) and potential customer loss.
  - 🛠️ **Technical Remediation:** Step-by-step fix instructions and production-ready HTML snippets.
- **Persistent Audit History:** Integrated **SQLite database** to store and retrieve full JSON results for historical tracking and comparison.
- **Modern SaaS Interface:** A clean, wide-layout dashboard built with **Streamlit**, featuring the **Inter** font and high-contrast professional styling.
- **Smart Validation:** Built-in URL regex validation and automatic HTTPS handling.

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **Browser Automation:** Playwright
- **Accessibility Engine:** Axe-core
- **AI Integration:** OpenAI API (GPT-4o-mini / GPT-4o)
- **Database:** SQLite
- **Frontend:** Streamlit (Custom CSS)

## 📦 Installation & Setup

### 1. Environment Setup

Clone the repository and create a dedicated virtual environment to ensure dependency isolation:

```bash
git clone <your-repository-url>
cd web-accessibility-ai

python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium
```

### 2. Configuration

The application uses environment variables for secure configuration. Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_sk_key_here
OPENAI_MODEL=gpt-4o-mini
```

### 3. Usage

1. **Launch the App:** Run `streamlit run app.py` in your terminal.
2. **Perform an Audit:** Enter a domain (e.g., `example.com`) in the sidebar and click **"Run Audit"**.
3. **Get AI Assistance:** Expand any violation in the results and click **"✨ Generate AI Insight"** for a comprehensive business and technical breakdown.
4. **Browse History:** Click on any previous audit in the **"Audit History"** section in the sidebar to instantly reload past results without re-scanning.

### 4. Data Privacy

- **Local Storage:** All audit data, including full JSON responses from the engine, is stored locally in a SQLite database (`audits.db`).
- **Security:** The database file and `.env` configuration are explicitly excluded from version control via `.gitignore` to ensure that sensitive API keys and private audit data are never leaked.

### 5. Self-Audit & Transparency

This tool has been audited using its own engine to ensure integrity and demonstrate professional transparency.

#### Known Issues (Framework Related)

As a prototype built on the Streamlit framework, certain accessibility violations are present in the generated HTML structure that cannot be directly modified within the Python layer:

- **`[ARIA-ALLOWED-ATTR]`:** The framework applies non-standard ARIA attributes to certain sidebar elements.
- **`[REGION]`:** Some framework-generated containers lack appropriate HTML5 landmarks.
- **`[COLOR-CONTRAST]`:** Certain default framework components (like info banners) may have sub-optimal contrast ratios.

#### Strategic Resolution

In a production environment, these issues would be resolved by migrating the frontend to a custom implementation (e.g., a dedicated web framework) to ensure 100% WCAG 2.2 compliance and full control over semantic HTML and ARIA roles.

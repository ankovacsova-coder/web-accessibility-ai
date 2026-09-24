from playwright.sync_api import Page, expect


def test_app_loads_correctly(page: Page):
    """Verifies that the main page loads and key content is visible."""
    page.goto("http://localhost:8501")

    expect(page).to_have_title("Accessibility Auditor")
    expect(page.get_by_text("Build a web that everyone can use")).to_be_visible()


def test_sidebar_is_present(page: Page):
    """Verifies that the sidebar and its main controls are visible."""
    page.goto("http://localhost:8501")

    expect(page.locator("section[data-testid='stSidebar']")).to_be_visible()
    expect(page.get_by_text("TARGET URL")).to_be_visible()
    expect(page.get_by_placeholder("example.com")).to_be_visible()
    expect(page.get_by_role("button", name="Run audit")).to_be_visible()
    expect(page.get_by_role("button", name="Clear")).to_be_visible()
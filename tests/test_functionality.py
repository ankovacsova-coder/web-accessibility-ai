from playwright.sync_api import Page, expect


def test_clear_button_resets_input(page: Page):
    """Ensures the Clear button successfully resets the URL input field."""
    page.goto("http://localhost:8501")

    input_field = page.get_by_placeholder("example.com")
    input_field.fill("test-url.com")

    page.get_by_role("button", name="Clear").click()
    expect(input_field).to_have_value("")


def test_audit_run_flow(page: Page):
    """Tests the end-to-end flow of running an accessibility audit."""
    page.goto("http://localhost:8501")

    input_field = page.get_by_placeholder("example.com")
    input_field.fill("google.com")

    page.get_by_role("button", name="Run audit").click()

    expect(page.get_by_text("Results for:")).to_be_visible(timeout=60000)
    expect(page.locator("code").filter(has_text="https://google.com")).to_be_visible(timeout=60000)
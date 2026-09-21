import asyncio
from playwright.async_api import async_playwright
from axe_playwright_python.async_playwright import Axe


async def run_audit(url):
    async with async_playwright() as p:
        # 1. Launch the browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"Starting accessibility audit for: {url}")

        # 2. Navigate to the target page
        await page.goto(url)

        # 3. Initialize and run the Axe accessibility audit
        axe = Axe()
        results = await axe.run(page)

        # 4. Convert results to a dictionary for easier access
        results_dict = results.response
        violations = results_dict.get("violations", [])

        print(f"Audit completed. Found {len(violations)} violations.")

        for i, violation in enumerate(violations, 1):
            # In a dictionary, we use string keys
            v_id = violation.get("id", "N/A")
            v_desc = violation.get("description", "No description provided")
            print(f"{i}. [{v_id}] - {v_desc}")

        # 5. Close the browser
        await browser.close()


# Main execution block for testing on a known accessibility test page
if __name__ == "__main__":
    target_url = "https://www.washington.edu/accesscomputing/AU/before.html"
    asyncio.run(run_audit(target_url))
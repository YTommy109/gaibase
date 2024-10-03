from playwright.sync_api import Playwright
from playwright.sync_api import sync_playwright


def run(playwright: Playwright) -> None:
    """セッティングページでアカウントを追加できる"""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('http://localhost:8501/')
    page.get_by_role('link', name='セッティング').click()
    page.locator('span').filter(has_text='アカウント').click()
    page.get_by_label('email').click()
    page.get_by_label('email').fill('sample@pwc.com')
    page.get_by_label('email').press('Tab')
    page.get_by_label('name').fill('sample taro')
    page.get_by_role('button', name='追加').click()
    page.locator('.dvn-scroller').click()
    page.locator('.dvn-scroller').click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

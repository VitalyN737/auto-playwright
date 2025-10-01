from playwright.sync_api import Page
from .sanitize_html import sanitize

def get_snapshot(page: Page) -> dict:
    """
    Takes a snapshot of the page, including the URL and sanitized HTML content.
    """
    html = page.content()
    sanitized_html = sanitize(html)

    return {
        "url": page.url,
        "html": sanitized_html,
    }
import asyncio
import pickle
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

COOKIE_FILE = "cookies.pkl"
URL_LOGIN = "https://authn.edx.org/login"
URL_SCRAPE = "https://learning.edx.org/course/course-v1:HarvardX+MCB63X+1T2024c/block-v1:HarvardX+MCB63X+1T2024c+type@sequential+block@b302fa451b5b46d9957b0a26ab08443b/block-v1:HarvardX+MCB63X+1T2024c+type@vertical+block@9fc58c08f3a649ec954b4ce2de67c3d3"

async def save_cookies(context):
    """Save cookies to a file."""
    cookies = await context.cookies()
    with open(COOKIE_FILE, "wb") as file:
        pickle.dump(cookies, file)

async def load_cookies(context):
    """Load cookies from a file if available."""
    try:
        with open(COOKIE_FILE, "rb") as file:
            cookies = pickle.load(file)
            if isinstance(cookies, list):  # Ensure it's a list of cookies
                await context.add_cookies(cookies)
    except FileNotFoundError:
        print("No saved cookies found. Logging in may be required.")

async def scrape_with_playwright():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True for headless mode
        context = await browser.new_context()
        page = await context.new_page()

        # Load cookies if available
        await load_cookies(context)

        # Go to login page
        await page.goto(URL_LOGIN)
        await asyncio.sleep(50)  # Allow manual login if necessary

        # Save cookies after logging in
        await save_cookies(context)

        # Navigate to the target page
        await page.goto(URL_SCRAPE)

        # Wait for content to load (adjust selector as needed)
        await page.wait_for_selector("#root", timeout=10000)

        # Get page content
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        print(soup.prettify())

        await browser.close()

# Run the Playwright scraping function
asyncio.run(scrape_with_playwright())

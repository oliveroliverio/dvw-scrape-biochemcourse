from pyppeteer import launch
import nest_asyncio
import asyncio

# Apply the fix for nested event loops
nest_asyncio.apply()


async def scrape_with_puppeteer():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://learning.edx.org/course/course-v1:HarvardX+MCB63X+1T2024c/home')

    # Wait for the content to load
    await page.waitForSelector('span.align-middle.col-6')
    element = await page.querySelector('span.align-middle.col-6')
    text = await page.evaluate('(el) => el.textContent', element)

    print(f'Text: {text}')
    await browser.close()

# Run directly
asyncio.run(scrape_with_puppeteer())

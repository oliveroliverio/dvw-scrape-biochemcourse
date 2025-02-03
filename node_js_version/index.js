
// it augments the installed puppeteer with plugin functionality
const puppeteer = require('puppeteer-extra')

// add stealth plugin and use defaults (all evasion techniques)
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer.use(StealthPlugin())

async function saveCookiesToFile(page, filePath) {
    try {
        // Getting the cookies from the current page
        const cookies = await page.cookies();

        // Writing the cookies to a file as JSON
        const fs = require('fs');
        fs.writeFileSync(filePath, JSON.stringify(cookies, null, 2));

        // Cookies have been saved successfully
        return true;
    } catch (error) {
        // An error occurred while saving cookies
        console.error('Error saving cookies:', error);
        return false;
    }
}

async function loadCookiesFromFile(page, filePath) {
    try {
        // Reading cookies from the specified file
        const fs = require('fs');
        const cookiesJson = fs.readFileSync(filePath, 'utf-8');
        const cookies = JSON.parse(cookiesJson);

        // Setting the cookies in the current page
        await page.setCookie(...cookies);
        // Cookies have been loaded successfully
        return true;
    } catch (error) {
        // An error occurred while loading cookies
        console.error('Error loading cookies:', error);
        return false;
    }
}

async function clearCookies(page, cookieNames = []) {
    try {
        if (cookieNames.length === 0) {
            // Clearing all cookies
            await page.evaluate(() => {
                document.cookie.split(';').forEach((cookie) => {
                    const name = cookie.split('=')[0].trim();
                    document.cookie = `${name}=; expires=Thu, 02 Jan 2024 00:00:00 UTC; path=/;`;
                });
            });
        } else {
            // Clearing specific cookies
            await page.deleteCookie(...cookieNames);
        }

        // Cookies have been cleared successfully
        return true;
    } catch (error) {
        // An error occurred while clearing cookies
        console.error('Error clearing cookies:', error);
        return false;
    }
}

async function run() {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto('https://books.toscrape.com/');

    // output html to console
    const html = await page.content();
    console.log(html);

    // const cookiesSaved = await saveCookiesToFile(page, 'cookies.json');
    // if (cookiesSaved) {
    //     console.log('Cookies saved successfully.');
    // } else {
    //     console.log('Failed to save cookies.');
    // }

    // await browser.close();
}

run();


//------------------resources---------------------
// cookie management in puppeteer: https://www.webshare.io/academy-article/puppeteer-cookies
// pretty-printing in bs4: https://www.geeksforgeeks.org/pretty-printing-in-beautifulsoup/


//------------------end resources---------------------


//------------------old code---------------------


// await page.waitForSelector('span.align-middle.col-6');
// const element = await page.$('span.align-middle.col-6');
// const text = await page.evaluate(el => el.textContent, element);
// console.log(text);
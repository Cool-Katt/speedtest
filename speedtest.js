require('dotenv').config()
const puppeteer = require('puppeteer')

const USERNAME_SELECTOR = "input[name='email']";
const PASSWORD_SELECTOR = "input[name='password']";
const LOGIN_SUBMIT_SELECTOR = '.auth0-lock-submit';
const CHECK_IF_TABLE_IS_FULL = 'tr:not(:first-child)';
const EXPORT_BUTTON_SELECTOR = '//span[contains(text(), "Export")]';
const XPATH_FIRST_LOGIN_BUTTON = '//span[contains(text(), "Login To Your Account")]'

async function speedtest() {
    const browser = await puppeteer.launch({product: 'firefox'});
    const page = await browser.newPage();
    await page.setDefaultTimeout(59000);
    await page.goto("http://reporting.speedtest.net/")
    const [login] = await page.$x(XPATH_FIRST_LOGIN_BUTTON)
    if (login) {
        await login.click()
        await page.waitForNavigation()
        await page.waitForSelector(LOGIN_SUBMIT_SELECTOR)
        await page.click(USERNAME_SELECTOR)
        await page.keyboard.type(process.env.SP_USER);
        await page.click(PASSWORD_SELECTOR)
        await page.keyboard.type(process.env.SP_PASSWORD);
        await page.click(LOGIN_SUBMIT_SELECTOR)
        await page.waitForNavigation()
        await page.goto('https://account.ookla.com/servers/reports')
    }
    await page.waitForSelector(CHECK_IF_TABLE_IS_FULL)
    const exportButton = await page.waitForXPath(EXPORT_BUTTON_SELECTOR)
    await pressDownloadButton(exportButton, page, '#web')
    await pressDownloadButton(exportButton, page, '#iphone')
    await pressDownloadButton(exportButton, page, '#android')
    //await page.screenshot({path: 'screenshot.png'})
    await browser.close()
}

async function pressDownloadButton(button, page, selector){
    await page.click('#techType')
    await page.click(selector)
    await button.click()
    await delay(30000)
}

function delay(time) {
    return new Promise(function(resolve) {
        setTimeout(resolve, time)
    });
}

speedtest().then(_ => 'finished')
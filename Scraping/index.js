// Adding Modules

const puppeteer = require("puppeteer");
const { mainSelect, scrapeData } = require("./scraper/scraper");

// Initializing Variables
const disease = "cough";
const URL = `https://www.healthline.com/search?q1=${disease}`;

// Functions running in parallel with other functions are called asynchronous
async function browserInit() {
  const browser = await puppeteer.launch(
    {
      headless: false,
      defaultViewport: null,
    },
    () => {
      console.log("Browser Loading Initiated");
    }
  );

  const page = await browser.newPage(); // opening browser in a new page
  await page.goto(URL); // going to the url
  await mainSelect(page); // calling the main select function in scrapper.js
}

browserInit();

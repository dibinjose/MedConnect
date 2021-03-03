const createCsvWriter = require("csv-writer").createObjectCsvWriter; // csv writer package
const csvwriter = createCsvWriter({
  path: "dataSet.csv",
  header: [
    {
      id: "disease",
      title: "DISEASE",
    },
    {
      id: "symptoms",
      title: "SYMPTOMS",
    },
  ],
  append: true, // if it is false, then the new data would overwrite the content in csv
  // fieldDelimiter: ";"
});

async function mainSelect(page, disease) {
  // Waits for the element to load
  console.log("Searching Initiated");
  await page.waitForSelector(
    "div.gsc-result:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)"
  );

  // Clicks on the element
  await page.click(
    "div.gsc-result:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)"
  );

  // await page.waitForSelector(
  //   "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(3) > ul:nth-child(5)"
  // );

  //Search for the particular disease to get particular selector
  if (disease === "cough" || disease === "fever") {
    await page.waitForSelector(
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(3) > ul:nth-child(5)"
    );
    const selector =
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(3) > ul:nth-child(5)";
    scrapeData(page, disease, selector);
  } else if (disease === "stomach ache") {
    await page.waitForSelector(
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(2) > ul:nth-child(7)"
    );
    const selector =
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(2) > ul:nth-child(7)";
    scrapeData(page, disease, selector);
  } else if (disease === "pneumonia") {
    await page.waitForSelector(
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(3) > ul:nth-child(4)"
    );
    const selector =
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(3) > ul:nth-child(4)";
    scrapeData(page, disease, selector);
  } else if (disease === "Diarrhea") {
    await page.waitForSelector(
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(2) > ul"
    );
    const selector =
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(2) > ul";
    scrapeData(page, disease, selector);
  } else if (disease === "Headaches") {
    await page.waitForSelector(
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div.css-2h0l1x > ul:nth-child(9)"
    );
    const selector =
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div.css-2h0l1x > ul:nth-child(9)";
    scrapeData(page, disease, selector);
  } else if (disease === "cancer") {
    await page.waitForSelector(
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(6) > ul:nth-child(4)"
    );
    const selector =
      "#__next > div.css-stl7tm > div > div > div:nth-child(3) > article > div:nth-child(6) > ul:nth-child(4)";
    scrapeData(page, disease, selector);
  }
}

//Scraping Module
async function scrapeData(page, disease, selector) {
  // console.log(selector);
  const cselect = selector;
  const Data = await page.evaluate((cselect) => {
    const list = document.querySelector(cselect); // the data we get is from ul li tags, which is not in array format

    const ListValue = Array.from(list.childNodes); //Converting NodeList to Array

    return ListValue.map((item) => {
      // map is used to iterate through the array
      return item.innerText;
    });
  }, cselect);
  console.log(Data);

  const records = [
    {
      disease: disease,
      symptoms: Data,
    },
  ];
  csvwriter
    .writeRecords(records) // returns a promise
    .then(() => {
      console.log("...Done");
    });
}

//exporting functions
module.exports.mainSelect = mainSelect;
module.exports.scrapeData = scrapeData;

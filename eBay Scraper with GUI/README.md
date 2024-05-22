# eBay Scraper with GUI

This Python script provides a graphical user interface (GUI) to scrape sold listings from eBay. It allows you to:

* Enter a search keyword for items you want to track.
* Filter results by listing type (All, Best Offer, Auction, Buy It Now).
* Set minimum/maximum price range and time filters.
* Easily export the scraped data into a CSV file named after your keyword.

## Features

* **User-Friendly GUI:** A simple interface makes it easy to input your search criteria.
* **Customizable Filters:**  Refine your search based on price, listing type, and time frame.
* **Data Export:**  Save results in a convenient CSV format for further analysis.
* **Error Logging:**  Logs any errors that occur during scraping to `error_log.txt`.

## Setup and Installation

1. **Prerequisites:**
   - **Python:** Ensure you have Python 3.x installed.
   - **Libraries:** Install the required Python libraries:
     ```bash
     pip install PyQt5 BeautifulSoup4 selenium python-dateutil
     ```
   - **ChromeDriver:** Download the appropriate ChromeDriver executable from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/) and place it in your project directory or add it to your system's PATH.

2. **Run:**
   - Execute the script: `python your_script_name.py`

## Usage

1. **Enter Keyword:** Type the name of the product or item you want to search for.
2. **Select Filter:** Choose the desired filter from the dropdown menu.
3. **(Optional) Adjust Settings:** Click "Settings" to customize price range and time filters.
4. **Click "Search":** The bot will start scraping eBay and save the results to a CSV file.

## Data Fields (CSV)

* Title
* Listing Type
* Price
* Number of Reviews (if available)
* eBay Listing URL

## Important Notes

* **eBay's Terms of Service:** Be mindful of eBay's terms of service and robots.txt file to avoid excessive scraping.
* **Rate Limiting:**  Implement rate limiting or delays in your code to prevent being blocked by eBay.
* **Data Usage:** Use the scraped data responsibly and ethically.

## Code Structure

The code is organized into the following sections:

- **Imports:** Imports necessary libraries.
- **Constants:** Defines the base eBay search URL and the ChromeDriver path.
- **`MainWindow` Class:** Handles the GUI elements and interactions.
- **Helper Functions:**
    - `init_driver()`: Initializes the Selenium WebDriver.
    - `scrape_ebay_data()`:  Performs the actual scraping logic.
    - `construct_url()`: Builds the complete eBay search URL based on the keyword and filters.
    - `settings()`: (Optional) Allows users to customize filters.
    - `menu()`: (Optional) The main interaction menu (not currently used in the provided code).
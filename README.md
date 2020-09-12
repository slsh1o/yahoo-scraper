# yahoo-scraper

## Requirements
To run this scraper you will first need:
- [WebDriver for Chrome](https://chromedriver.chromium.org/downloads)

**Note:** WebDriver should be added to your system `Path`.

## Installation
When requirements are satisfied you can clone this repo and run `pip install -r requirements.txt`.

## Usage
Now that everything installed you could run scraper by issuing `python scraper.py` in your terminal.

### Options
You can manually define desired options in `scraper.py`.
- Set `options.headless = True` if you want run scraper in `Headless mode` (default `False`)
- Set path to your `WebDriver` by setting `webdriver_path='/path/to/chromedriver'`

import time
import csv

from os import mkdir
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from calculate_3dbc import calculate_all_files


COMPANY_LIST = ('PD', 'ZUO', 'PINS', 'ZM', 'PVTL', 'DOCU', 'CLDR', 'RUN')

# Get current dir
DATA_DOWNLOAD_DIR = Path(__file__).resolve().with_name('historical_data')
NEWS_DOWNLOAD_DIR = Path(__file__).resolve().with_name('last_news')


# Set up chrome settings to auto download
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    'download.default_directory': f'{DATA_DOWNLOAD_DIR}',
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
})
# Headless mode
options.headless = True

# Set up webdriver
driver = webdriver.Chrome(options=options)
driver.get('https://finance.yahoo.com/')

wait = WebDriverWait(driver, 5)


def _get_last_news():
    """Scrape last news from `Summary` page of the company."""
    # Wait until company page will load
    # by waiting for news list rendered on page
    news_stream_list = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="quoteNewsStream-0-Stream"]/ul'))
    )

    # Some time to get yahoo load news
    time.sleep(2)

    # Get titles and links for news & save them to csv file
    with open(f'{NEWS_DOWNLOAD_DIR / company}_last_news.csv', mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['link', 'title'])
        writer.writeheader()

        for el in news_stream_list.find_elements_by_xpath('.//descendant::h3[@class="Mb(5px)"]'):
            writer.writerow({
                'title': el.text,
                'link': el.find_element_by_tag_name('a').get_attribute('href')
            })

    print(f'Saved last news for {company}')


def _get_historical_data():
    """
    Action chain which goes to `Historical Data` page
    of the company, set max date range and download data.
    """
    # Click on `Historical Data` btn
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="quote-nav"]/ul/li[6]/a'))
    ).click()

    # Wait until `date dropdown menu` appear
    # click on it to get `Max` btn
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,
             '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div')
        )
    ).click()

    # Click on `Max` btn
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,
             '//*[@id="dropdown-menu"]/div/ul[2]/li[4]/button')
        )
    ).click()

    # Click `Apply` to set date range
    driver.find_element_by_xpath(
        '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button'
    ).click()

    # Finally click on `Download` btn
    # to get file with Historical Data
    driver.find_element_by_xpath(
        '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a'
    ).click()

    ActionChains(driver).perform()

    print(f'Downloaded historical data for {company}')

    time.sleep(1)


# =========
# Script ->
# =========

# Init dirs
# Create dir for `Historical Data`
try:
    mkdir(DATA_DOWNLOAD_DIR)
except FileExistsError:
    pass

# Create dir for `Last News`
try:
    mkdir(NEWS_DOWNLOAD_DIR)
except FileExistsError:
    pass

# Loop goes through company list
# perform searching of companies and call
# functions above to get last news
# and historical data
for company in COMPANY_LIST:
    # Select search field and pass company name to it
    search_field = wait.until(
        EC.presence_of_element_located(
            (By.ID, 'yfin-usr-qry')
        )
    )
    search_field.clear()
    search_field.send_keys(company)

    # Check if passed company exist
    try:
        # Wait until dropdown menu with companies list appear
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    'modules_quoteSymbol__3Vtbg'
                 ))
        )
    except TimeoutException:
        print(f'"{company}" not found. Skip it.')
        continue
    search_field.send_keys(Keys.RETURN)

    try:
        _get_last_news()
        _get_historical_data()
    except Exception as exc:
        print(f'Something goes wrong with {company}!')

time.sleep(2)
driver.quit()

# Calculate `3day_before_change` data for downloaded files
calculate_all_files(DATA_DOWNLOAD_DIR)

print('Calculated `3day_before_change` for all files')

print('>Test Task DONE')

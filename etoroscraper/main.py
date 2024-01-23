from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd
import time

from config import Config
from login import login
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


if __name__ == '__main__':

    print(Config.BASE)
    print(Config.MARKETS)
    print(Config.EXCHANGES)

    # Start Chrome Driver
    options = uc.ChromeOptions()
    options.headless = False  # Set headless to False to run in non-headless mode

    # Login
    driver = uc.Chrome(use_subprocess=True, options=options)
    login(driver, Config.LOGIN)

    # SCRAPE STOCKS

    for exchange in Config.EXCHANGES:
        print(exchange)
        driver.get(exchange)
        input('Exchange Loaded?')
        time.sleep(5)
        xp_rows = '//*[@automation-id="discover-market-results-row"]'
        rows = driver.find_elements(By.XPATH, xp_rows)
        for row in rows:
            xp_tick = '//*[@automation-id="trade-item-name"]'
            xp_name = '//*[@automation-id="trade-item-full-name"]'
            ticker = row.find_element(By.XPATH, xp_tick).text
            name = row.find_element(By.XPATH, xp_name).text
            print(f'{ticker}, {name}')
    driver.close()

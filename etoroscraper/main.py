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

    # Start Chrome Driver
    options = uc.ChromeOptions()
    # Set headless to False to run in non-headless mode
    options.headless = False

    # Login page
    driver = uc.Chrome(use_subprocess=True, options=options)
    login(driver, Config.LOGIN)
    input('PRESS ENTER AFTER LOGGING IN')
    # SCRAPE STOCKS
    for exchange in Config.EXCHANGES:
        print(exchange)

        driver.get(exchange)

        input('Exchange Loaded?')
        time.sleep(5)

        num_items = driver.find_element(By.XPATH, '//*[@automation-id="discover-market-results-num"]')
        num_items = int(num_items.text.replace(',', ''))
        print(f'{num_items} items found')

        next_button = driver.find_element(By.XPATH, '//*[@automation-id="discover-market-next-button"]')

        stocks = []
        while True:
            counted = 0
            xp_rows = '//*[@automation-id="trade-item-info"]'
            rows = driver.find_elements(By.XPATH, xp_rows)

            for row in rows:
                xp_tick = './/*[@automation-id="trade-item-name"]'
                xp_name = './/*[@automation-id="trade-item-full-name"]'
                ticker = row.find_element(By.XPATH, xp_tick).text
                name = row.find_element(By.XPATH, xp_name).text
                stocks.append((ticker, name))
                print(f'{ticker}, {name}')
                counted += 1

            num_items -= counted
            print(f'{counted} counted items in this page\n'
                  f'{num_items} items remaining\n'
                  f'{len(stocks)} item collected')

            if num_items <= 0:
                break
            else:
                next_button.click()
            input('PRESS ENTER WHEN PAGE IS LOADED')
            time.sleep(2)

    driver.close()

from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd
import time

from config import Config
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def login(driver, login_page):
    # Read user and password
    with open('logindata.csv', 'r') as log_data:
        username, password = log_data.read().split(',')
        log_data.close()

    # Get login page
    driver.get(login_page)
    # Select form item
    user_field = driver.find_element(By.XPATH, '//*[@id="username"]')
    passw_field = driver.find_element(By.XPATH, '//*[@id="password"]')
    sign_in_btn = driver.find_element(By.XPATH, '//*[@automation-id="login-sts-btn-sign-in"]')

    # Fill form
    time.sleep(2)
    user_field.send_keys(username)
    time.sleep(2)
    passw_field.send_keys(password)

    # Click sign in
    time.sleep(2)
    sign_in_btn.click()


def main():

    # Start Chrome Driver
    options = uc.ChromeOptions()

    # Set headless to False to run in non-headless mode
    options.headless = False

    # Login page
    driver = uc.Chrome(use_subprocess=True, options=options)
    login(driver, Config.LOGIN)
    input('PRESS ENTER AFTER LOGGING IN')

    # SCRAPE STOCKS
    stocks = []
    for exc_row in Config.MARKETS.iterrows():
        exchange = exc_row[1].LINK
        exc_name = exc_row[1].NAME
        exc_cat = exc_row[1].CATEGORY
        print(exchange)
        driver.get(exchange)
        # input('Exchange Loaded?')
        time.sleep(5)

        num_items = driver.find_element(By.XPATH, '//*[@automation-id="discover-market-results-num"]')
        num_items = int(num_items.text.replace(',', ''))
        print(f'{num_items} items found')

        next_button = None
        if num_items > 50:
            next_button = driver.find_element(By.XPATH, '//*[@automation-id="discover-market-next-button"]')


        while True:
            counted = 0
            xp_rows = '//*[@automation-id="trade-item-info"]'
            rows = driver.find_elements(By.XPATH, xp_rows)

            for row in rows:
                xp_tick = './/*[@automation-id="trade-item-name"]'
                xp_name = './/*[@automation-id="trade-item-full-name"]'
                ticker = row.find_element(By.XPATH, xp_tick).get_attribute('innerHTML')
                idx = ticker.find(' ')
                ticker = ticker[:idx]

                name = row.find_element(By.XPATH, xp_name).get_attribute('innerHTML').replace(',', '')
                if name == '':
                    name = ticker

                print(f'{exc_cat}, {exc_name}, {name},  {ticker}')
                stocks.append([exc_cat, exc_name, name,  ticker])
                counted += 1

            num_items -= counted
            print(f'{counted} counted items in this page\n'
                  f'{num_items} items remaining\n'
                  f'{len(stocks)} item collected')

            if num_items <= 0:
                break
            elif next_button is not None:
                pop_xp = '//*[@id="cdk-overlay-0"]/et-dialog-container/et-pre-push/div/div[1]/a'
                pop = driver.find_element(By.XPATH, pop_xp)
                try:
                    pop.click()
                except:
                    pass
                next_button.click()
            time.sleep(3)

    stocks = pd.DataFrame(stocks, columns=['CATEGORY', 'EXCHANGE', 'NAME', 'ETORO_TICKER'])
    stocks.to_csv(f'download/e_toro.csv', index=False)

    driver.close()


if __name__ == '__main__':
    main()

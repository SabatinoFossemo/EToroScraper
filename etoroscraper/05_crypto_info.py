import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time

pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

YAHOO = 'https://finance.yahoo.com/quote/'


def get_yahoo():
    # Start Chrome Driver
    options = uc.ChromeOptions()

    # Set headless False to run in non-headless mode
    options.headless = False

    # Get Yahoo
    driver = uc.Chrome(use_subprocess=True, options=options)
    driver.get(YAHOO)
    cookies_xp = '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[2]'
    cookies = driver.find_element(By.XPATH, cookies_xp)
    cookies.click()
    time.sleep(2)
    return driver


def main():
    etoro = pd.read_csv('download/etoro_CRYPTO.csv')
    etoro['YAHOO_TICKER'] = etoro.ETORO_TICKER + '-USD'
    driver = get_yahoo()
    for coin in etoro.YAHOO_TICKER:
        profile = f'{YAHOO}{coin}'
        driver.get(profile)
        time.sleep(0.5)
        print(f'{coin} - {driver.current_url}')
    # etoro.to_csv('download/etoro_CRYPTO.csv', index=False)

if __name__ == '__main__':
    main()
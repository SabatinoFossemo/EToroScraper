import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time


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


def get_value(driver, type_val, xpath, error):
    try:
        value = driver.find_element(By.XPATH, xpath).text
    except:
        error = True
        value = 'NotFound'

    if type_val == 'int':
        try:
            value = int(value.replace(',', ''))
        except:
            value = 0
    elif type_val == 'str':
        value = str(value)

    return value, error


def get_info(ticker):
    driver = get_yahoo()

    profile = f'{YAHOO}{ticker}/profile?p={ticker}'
    driver.get(profile)

    error_trigger = False

    if profile != driver.current_url:
        error_trigger = True

    time.sleep(0.5)

    sector, error_trigger = get_value(driver, 'str',
                                      '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[2]',
                                      error_trigger)
    industry, error_trigger = get_value(driver, 'str',
                                        '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]',
                                        error_trigger)
    employees, error_trigger = get_value(driver, 'int',
                                         '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[6]/span',
                                         error_trigger)

    # if error_trigger:
    #     input(f'ERROR {ticker}')

    driver.quit()

    return sector, industry, employees


def main():
    etoro = pd.read_csv('download/e_toro.csv')

    _i = input('press N to create new file: ')
    if _i == 'N':
        info = pd.read_csv('download/info_file.csv')
        info['YAHOO_TICKER'] = '_'
    else:
        info = pd.read_csv('download/new_info.csv')

    for row in info.iterrows():
        print(row[0])
        i = row[1]

        if i.YAHOO_TICKER != '_':
            continue

        if i.SECTOR != 'NotFound':
            info.at[row[0], 'YAHOO_TICKER'] = i.ETORO_TICKER
        else:
            if i.YAHOO_TICKER == '_':
                print(etoro[etoro.ETORO_TICKER == i.ETORO_TICKER])
                y_t = ''

                if i.ETORO_TICKER.endswith('.NV'):
                    y_t = f'{i.ETORO_TICKER[:-2]}AS'
                    print(y_t)

                else:
                    y_t = input('Insert Yahoo Ticker: ')

                sector = 'NotFound'
                industry = 'NotFound'
                employee = 'NotFound'
                if y_t != '':
                    sector, industry, employee = get_info(y_t)
                else:
                    y_t = 'NotFound'
                info.at[row[0], 'YAHOO_TICKER'] = y_t
                info.at[row[0], 'SECTOR'] = sector
                info.at[row[0], 'INDUSTRY'] = industry
                info.at[row[0], 'EMPLOYEES'] = employee

        info.to_csv(f'download/new_info.csv', index=False)
        print(info)


if __name__ == '__main__':
    main()

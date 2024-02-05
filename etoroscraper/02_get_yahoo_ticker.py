from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import time

pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

YAHOO = 'https://finance.yahoo.com/quote/'


def create_file(info_file_name, error_file_name):
    info_file = pd.DataFrame(columns=['ETORO_TICKER', 'SECTOR', 'INDUSTRY', 'EMPLOYEES'])
    info_file.to_csv(info_file_name, index=False)
    error_file = pd.DataFrame(columns=['CATEGORY', 'EXCHANGE', 'NAME', 'ETORO_TICKER'])
    error_file.to_csv(error_file_name, index=False)


def load_file(info_file_name, error_file_name):
    file = pd.read_csv(info_file_name)
    pd.read_csv(error_file_name)
    return file


def append_file(row, file_name):
    row.to_csv(file_name, mode='a', index=False, header=False)


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
            value = type_val(value)
        except:
            value = 0
    elif type_val == 'str':
        value = str(value)

    return value, error


def main():

    info_file_name = 'download/info_file.csv'
    error_file_name = 'download/error.csv'
    df = pd.read_csv('download/e_toro.csv')

    start_row = 0
    _i = input('Press N to create a new file else ENTER: ')
    if _i == 'N':
        create_file(info_file_name, error_file_name)
    else:
        file = load_file(info_file_name, error_file_name)
        start_row = len(file.index)
        print(f'Start from line {start_row}\n'
              f'Previous line:\n{df.iloc[start_row-1]}\n'
              f'Next:\n{df.iloc[start_row]}')
        input('Press ENTER to start')

    for row in df[df.CATEGORY == 'STOCK'].iloc[start_row:].iterrows():
        # Get Yahoo driver
        driver = get_yahoo()

        name = row[1].NAME
        etoro_ticker = row[1].ETORO_TICKER

        profile = f'{YAHOO}{etoro_ticker}/profile?p={etoro_ticker}'
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

        if error_trigger:
            print(row[1])
            error = pd.DataFrame([row[1]])
            append_file(error, error_file_name)

        info_row = pd.DataFrame([[etoro_ticker, sector, industry, employees]])
        append_file(info_row, info_file_name)
        print(f'"{etoro_ticker}", "{name}", "{sector}", "{industry}", ({employees})')

        driver.quit()


if __name__ == '__main__':
    main()

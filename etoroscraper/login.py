from selenium.webdriver.common.by import By
import time


def login(driver, login_page):
    driver.get(login_page)
    user = driver.find_element(By.XPATH, '//*[@id="username"]')
    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    time.sleep(2)
    user.send_keys('ksher83')
    time.sleep(2)
    password.send_keys('UnderR00m1')
    input('PRESS ENTER TO CONTINUE')

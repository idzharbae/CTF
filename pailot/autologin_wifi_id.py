from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

CONNECTION_CHECK_INTERVAL = 15
TIMEOUT_SECOND = 20
LOGIN_PAGE_URL = 'https://welcome2.wifi.id/wms/?....'
PASSWORD = '...'

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def connect_to_wifi(wifi_login_page_url, password_str):
    # uncomment when script done
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(15)

    driver.get(wifi_login_page_url)

    try:
        element = WebDriverWait(driver, TIMEOUT_SECOND).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-header"))
        )
        print('[+] No login required, exiting...')
    except:
        print('[-] Login required')
        
        try:
            element = WebDriverWait(driver, TIMEOUT_SECOND).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
        except:
            print('[-] Failed to get username form input')
            driver.quit()
            return
        
        driver.find_element_by_css_selector("#username").send_keys(password_str)
        driver.find_element_by_css_selector(".button-lg").click()
        
        try:
            element = WebDriverWait(driver, TIMEOUT_SECOND).until(
                EC.presence_of_element_located((By.CLASS_NAME, "success-header"))
            )
        except:
            print("Unexpected error:", sys.exc_info()[0])
    finally:
        driver.quit()

while True:
    if ping('google.com'):
        print('[+] Wifi is OK')
    else:
        print('[-] Wifi disconnected, trying to login...')
        connect_to_wifi(LOGIN_PAGE_URL, PASSWORD)
    time.sleep(CONNECTION_CHECK_INTERVAL)


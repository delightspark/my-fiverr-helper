import time
import random
import json
import os
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

FIVERR_URL = "https://www.fiverr.com/"
DASHBOARD_URL = "https://www.fiverr.com/users/delightspark/manage_gigs"
COOKIE_FILE = "fiverr_cookies.json"

PROXY_HOST = os.environ.get("PROXY_HOST" )
PROXY_PORT = os.environ.get("PROXY_PORT")
PROXY_USER = os.environ.get("PROXY_USER")
PROXY_PASS = os.environ.get("PROXY_PASS")

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    sw_options = {}
    if PROXY_HOST:
        sw_options = {
            'proxy': {
                'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
                'https': f'https://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
            }
        }

    driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=sw_options )
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    return driver

def load_cookies(driver):
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                # Fix "sameSite" for Selenium compatibility
                if 'sameSite' in cookie:
                    mapping = {"no_restriction": "None", "lax": "Lax", "strict": "Strict"}
                    cookie['sameSite'] = mapping.get(cookie['sameSite'].lower(), cookie['sameSite'])
                
                # Remove extra fields that Selenium doesn't use
                cookie.pop('expirationDate', None)
                cookie.pop('hostOnly', None)
                cookie.pop('session', None)
                cookie.pop('storeId', None)
                
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Skipped a cookie: {cookie.get('name')} - {e}")
        return True
    return False

def run():
    driver = None
    try:
        driver = setup_driver()
        driver.get(FIVERR_URL)
        time.sleep(5)
        if load_cookies(driver):
            print("Cookies loaded. Refreshing...")
            driver.refresh()
            time.sleep(7)
            driver.get(DASHBOARD_URL)
            time.sleep(10)
            if "login" in driver.current_url.lower():
                print("Session expired or failed.")
            else:
                print(f"SUCCESS! Currently on: {driver.current_url}")
        else:
            print("No cookie file found.")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run()

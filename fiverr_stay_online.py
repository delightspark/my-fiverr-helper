import time
import random
import pickle
import os
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

FIVERR_URL = "https://www.fiverr.com/"
DASHBOARD_URL = "https://www.fiverr.com/users/delightspark/manage_gigs"
COOKIE_FILE = "fiverr_cookies.pkl"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

PROXY_HOST = os.environ.get("PROXY_HOST")
PROXY_PORT = os.environ.get("PROXY_PORT")
PROXY_USER = os.environ.get("PROXY_USER")
PROXY_PASS = os.environ.get("PROXY_PASS")

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={USER_AGENT}")
    chrome_options.add_argument("--window-size=1920,1080")

    seleniumwire_options = {}
    if PROXY_HOST and PROXY_PORT and PROXY_USER and PROXY_PASS:
        seleniumwire_options = {
            'proxy': {
                'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
                'https': f'https://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

    driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options )
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    return driver

def load_cookies(driver, path):
    if os.path.exists(path):
        with open(path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                if ".fiverr.com" in cookie["domain"] or "fiverr.com" == cookie["domain"]:
                    try: driver.add_cookie(cookie)
                    except: pass
        return True
    return False

def run_automation():
    driver = None
    try:
        driver = setup_driver()
        driver.get(FIVERR_URL)
        time.sleep(5)
        if load_cookies(driver, COOKIE_FILE):
            driver.refresh()
            time.sleep(5)
            driver.get(DASHBOARD_URL)
            time.sleep(10)
            print("Session active.")
        else:
            print("No cookies found.")
    except Exception as e: print(f"Error: {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_automation()

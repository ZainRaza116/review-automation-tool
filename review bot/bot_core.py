import random
from itertools import cycle
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import subprocess
import shutil
import csv
import undetected_chromedriver as uc
import json

def kill_chrome_processes():
    print("Cleaning up Chrome processes...")
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], 
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL)
        subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'],
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL)
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error killing Chrome processes: {str(e)}")
        return False

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
]

# Device profiles with realistic specifications
DEVICE_PROFILES = [
    {
        "name": "Windows Desktop",
        "viewport_width": 1920,
        "viewport_height": 1080,
        "pixel_ratio": 1,
        "platform": "Windows",
    },
    {
        "name": "MacBook Pro",
        "viewport_width": 1440,
        "viewport_height": 900,
        "pixel_ratio": 2,
        "platform": "MacIntel",
    },
    {
        "name": "iPhone 13",
        "viewport_width": 390,
        "viewport_height": 844,
        "pixel_ratio": 3,
        "platform": "iPhone",
    },
    {
        "name": "iPad Pro",
        "viewport_width": 1024,
        "viewport_height": 1366,
        "pixel_ratio": 2,
        "platform": "iPad",
    }
]

def generate_random_device():
    """Generate random device characteristics and return Chrome options"""
    device = random.choice(DEVICE_PROFILES)
    user_agent = random.choice(USER_AGENTS)
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument(f"--user-agent={user_agent}")
    chrome_options.add_argument(f"--window-size={device['viewport_width']},{device['viewport_height']}")
    
    # Add random language and timezone
    languages = ["en-US", "en-GB", "en-CA", "en-AU"]
    timezones = ["America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney"]
    chrome_options.add_argument(f"--lang={random.choice(languages)}")
    chrome_options.add_argument(f"--timezone={random.choice(timezones)}")
    
    return chrome_options, device

def start_chrome_with_proxy(proxy):
    print(f"Initializing Chrome with proxy: {proxy}")

    
    kill_chrome_processes()

    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f'--user-agent={user_agent}')
    
    proxy_host = "ma.smartproxy.com"
    proxy_port = "40003"
    proxy_user = "sp91cq7av8"
    proxy_pass = "ymUlL8g1qw2+vT1Lmf"
    proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    chrome_options.add_argument(f"--proxy-server={proxy_url}")
    
    try:
        # service = ChromeService(ChromeDriverManager().install())
        driver = uc.Chrome()
        widths = [1366, 1440, 1920]
        heights = [768, 900, 1080]
        driver.set_window_size(random.choice(widths), random.choice(heights))
        
        print(f"Started browser with User-Agent: {user_agent}")
        return driver
    except Exception as e:
        print(f"Error starting Chrome: {str(e)}")
        raise

def kill_chrome_processes():
    print("Cleaning up Chrome processes...")
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], 
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL)
        subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'],
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL)
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error killing Chrome processes: {str(e)}")
        return False

def login_to_google(driver, email, password, recovery_email ):
    try:
        print(f"Attempting to login with email: {email}")
        driver.get("https://accounts.google.com/signin")
        time.sleep(3)
        wait = WebDriverWait(driver, 15)
        
        # Enter email
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "identifier")))
        email_field.send_keys(email)
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]/..")))
        next_button.click()
        time.sleep(3)
        
        # Enter password
        password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
    )
        password_field.send_keys(password)
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]/..")))
        next_button.click()
        time.sleep(5)

        recovery_email_item = driver.find_element(By.XPATH, "//li[.//div[contains(text(), 'Confirm your recovery email')]]")
        recovery_email_item.click()
        time.sleep(5)

        email_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@aria-label, 'Enter recovery email address')]")))
        email_input.send_keys(recovery_email)
        next_button = driver.find_element(By.XPATH, "//button[.//span[text()='Next']]")
        next_button.click()
        time.sleep(5)
        
        
        return True
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False

def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def post_review(driver, review_link, comments):
    try:
        driver.get(review_link)
        time.sleep(5)

        wait = WebDriverWait(driver, 15)

        review_button = driver.find_element(By.XPATH, "//button[.//div[contains(text(), 'Reviews')]]")
        review_button.click()
        time.sleep(2)

        write_review_button = driver.find_element(By.XPATH, "//button[@aria-label='Write a review']//span[@class='DVeyrd ']")
        write_review_button.click()
        time.sleep(2)
        
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@name='goog-reviews-write-widget']")))
        
        star_selectors = [
            "//div[@class='s2xyy' and @aria-label='Five stars']",
            "//div[contains(@class, 's2xyy')][5]",
            "//div[@aria-label='Five stars']",
            "//div[contains(@class, 'rating-star')][5]"
        ]
        
        for selector in star_selectors:
            try:
                star_element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                driver.execute_script("arguments[0].click();", star_element)
                break
            except:
                continue

        text_area = driver.find_element(By.XPATH, "//textarea[@aria-label='Enter review']")
        review = random.choice(comments)
        text_area.send_keys(review)
        time.sleep(2)

        submit_button = driver.find_element(By.XPATH, "//button[@jsname='IJM3w']")
        submit_button.click()
        time.sleep(3)
        
        return True
    except Exception as e:
        print(f"Error posting review: {str(e)}")
        return False

def read_accounts(filename):
    accounts = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 3:
                accounts.append({
                    'email': parts[0],
                    'password': parts[1],
                    'recovery_email': parts[2]
                })
    return accounts

def bot(accounts_file, proxies_file, review_links_file, comments_file):
    accounts = read_accounts(accounts_file)
    proxies = read_file_lines(proxies_file)
    review_links = read_file_lines(review_links_file)
    comments = read_file_lines(comments_file)
    
    print(f"\nStarting bot with:")
    print(f"Total accounts: {len(accounts)}")
    print(f"Total proxies available: {len(proxies)}")
    print(f"Total review links: {len(review_links)}")
    
    proxy_cycle = cycle(proxies)
    total_reviews = 0
    
    for account in accounts:
        print(f"\nProcessing account: {account['email']}")
        proxy = next(proxy_cycle)
        driver = None
        try:
            driver = start_chrome_with_proxy(proxy)
            if login_to_google(driver, account['email'], account['password'], account['recovery_email']):
                account_reviews = 0
                for review_link in review_links:
                    if post_review(driver, review_link, comments):
                        account_reviews += 1
                        total_reviews += 1
                        print(f"Successfully posted review for: {review_link}")
                    time.sleep(random.uniform(30, 60))  # Random delay between reviews
                print(f"Account {account['email']} completed {account_reviews} reviews")
            else:
                print(f"Failed to login with account: {account['email']}")
        except Exception as e:
            print(f"Error occurred with account {account['email']}: {str(e)}")
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            kill_chrome_processes()
        
        time.sleep(random.uniform(60, 120))  # Random delay between accounts
    
    print(f"\nBot finished. Total reviews completed: {total_reviews}")

if __name__ == "__main__":
    accounts_file = 'accounts.txt'  
    proxies_file = 'proxies.txt'
    review_links_file = 'review_links.txt'
    comments_file = 'comments.txt'
    
    bot(accounts_file, proxies_file, review_links_file, comments_file)
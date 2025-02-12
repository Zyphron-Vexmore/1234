import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver as wire_webdriver  # Import selenium-wire webdriver
# from webdriver_manager.chrome import ChromeDriverManager

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = "7244502796:AAHPRBZlUFIQS3HbF7ZgKixHXPJxLi4bBqg"
TELEGRAM_CHAT_ID = "1005895910"

# Proxy configuration
PROXY_HOSTS = [
    "45.39.206.197",
    "104.253.151.165",
    "45.39.206.150",
    "45.39.206.59",
    "104.253.151.157",
    "45.39.206.158",
    "45.39.206.116",
    "45.39.206.140",
    "45.39.206.143",
    "213.204.18.134"
]
PROXY_PORT = "50100"
PROXY_USER = "helmostafi"
PROXY_PASS = "qeJb56Yns4"

def send_telegram_message(message):
    """Send a message to the specified Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Message sent to Telegram successfully!")
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

def setup_driver(proxy_host):
    """Initialize Selenium WebDriver with proxy and auto-install ChromeDriver."""
    
    # Configure proxy settings
    seleniumwire_options = {
        "proxy": {
            "http": f"http://{PROXY_USER}:{PROXY_PASS}@{proxy_host}:{PROXY_PORT}",
            "https": f"https://{PROXY_USER}:{PROXY_PASS}@{proxy_host}:{PROXY_PORT}",
        }
    }

    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Automatically install the latest ChromeDriver
    driver = wire_webdriver.Chrome(
        seleniumwire_options=seleniumwire_options,
        options=options
    )
    
    driver.maximize_window()
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 10)
    return driver, wait

keywords = [
    "Ceramica Sassuolo",
    "Gres porcellanato sassuolo",
    "Vendita diretta pavimenti",
    "Sassuolo ceramica plus",
    "Produzione e vendita diretta piastrelle",
    "Show-room ceramiche sassuolo"
]

def search_and_click(proxy_host):
    """Search for a keyword and click a Google ad, sending results to Telegram."""
    for keyword in keywords:
        driver, wait = setup_driver(proxy_host)
        
        try:
            # Step 1: Open Google
            driver.get("http://www.google.it")
            time.sleep(random.uniform(2, 4))

            # Get public IP address
            ip_address = driver.execute_script("return fetch('https://api64.ipify.org?format=json').then(res => res.json()).then(data => data.ip);")
            time.sleep(2)

            # Accept cookies if pop-up appears
            try:
                time.sleep(5)
                accept_button = wait.until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="L2AGLb"]/div'))
                )
                accept_button.click()
                time.sleep(random.uniform(2, 5))
            except:
                print("No cookie pop-up found.")

            # Step 2: Perform search
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(keyword)
            time.sleep(random.uniform(1, 3))
            search_box.send_keys(Keys.RETURN)
            time.sleep(random.uniform(3, 6))

            # Step 3: Find Sponsored Ads
            ads = driver.find_elements(By.XPATH, "//span[contains(text(),'Sponsorizzato')]/ancestor::div[1]//a")

            if ads:
                ad_link = ads[0].get_attribute("href")  # Get ad link
                print(f"Clicking ad: {ad_link}")
                ads[0].click()
                time.sleep(random.uniform(5, 10))  # Wait for page to load
                
                message = f"✅ Ad Found!\n🔍 Keyword: {keyword}\n🌍 IP: {ip_address}\n🔗 Ad Link: {ad_link}"
            else:
                print("No Google Ads found!")
                message = f"❌ No Ad Found!\n🔍 Keyword: {keyword}\n🌍 IP: {ip_address}"

            send_telegram_message(message)

        except Exception as e:
            print("An error occurred:", e)

        finally:
            time.sleep(5)  # Reduce wait time
            driver.quit()

if __name__ == "__main__":
    for host in PROXY_HOSTS:
        search_and_click(host)

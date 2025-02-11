from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver as wire_webdriver  # Import selenium-wire webdriver
from webdriver_manager.chrome import ChromeDriverManager

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
    # options.add_argument("--headless=new")  # Enable headless mode for automation
    # options.add_argument("--no-sandbox")  
    # options.add_argument("--disable-dev-shm-usage")  
    # options.add_argument("--window-size=1920,1080")

    # Automatically install the latest ChromeDriver
    driver = wire_webdriver.Chrome(
        seleniumwire_options=seleniumwire_options,
        options=options
    )
    
    driver.maximize_window()
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 10)
    return driver, wait


def simulate_human_behavior(driver):
    """Simulate mouse movements and scrolling to mimic human behavior."""
    actions = ActionChains(driver)
    body = driver.find_element(By.TAG_NAME, 'body')
    
    # Random scrolling
    scrolls = random.randint(2, 5)
    for _ in range(scrolls):
        scroll_amount = random.randint(300, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(1, 3))

    # Simulate mouse movement with hesitation
    width, height = driver.get_window_size().values()
    for _ in range(random.randint(5, 10)):
        x_offset = random.randint(0, width)
        y_offset = random.randint(0, height)
        actions.move_by_offset(x_offset / random.uniform(1.1, 2.0), y_offset / random.uniform(1.1, 2.0)).perform()
        time.sleep(random.uniform(0.5, 1.5))


keywords = [
    "Ceramica Sassuolo",
    "Gres porcellanato sassuolo",
    "Vendita diretta pavimenti",
    "Sassuolo ceramica plus",
    "Produzione e vendita diretta piastrelle",
    "Show-room ceramiche sassuolo"
]

def search_and_click(proxy_host):
    """Search for a keyword and click a Google ad."""
    for keyword in keywords:
        driver, wait = setup_driver(proxy_host)
        
        try:
            # Step 1: Open Google
            driver.get("http://www.google.it")
            time.sleep(random.uniform(2, 4))

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
                ad_link = ads[0]  # Click the first sponsored ad
                print(f"Clicking ad: {ad_link.get_attribute('href')}")
                ad_link.click()
                time.sleep(random.uniform(5, 10))  # Wait for page to load
            else:
                print("No Google Ads found!")

        except Exception as e:
            print("An error occurred:", e)

        finally:
            time.sleep(5)  # Reduce wait time
            driver.quit()


if __name__ == "__main__":
    for host in PROXY_HOSTS:
        search_and_click(host)

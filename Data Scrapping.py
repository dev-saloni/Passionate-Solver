from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--headless=new") 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

main_url = 'https://acma.in/'
driver.get(main_url)

def get_company_names():
    select_element = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/section[5]/div/div/div[1]/div[2]/form/div[2]/div/select")))
    select = Select(select_element)
    return list(map(lambda option: option.text.strip(), select.options[1:]))

company_names = get_company_names()

def scrape_company_data(company_name):
    try:
        print(f"Scraping: {company_name}")
        driver.get(main_url)

        select_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/section[5]/div/div/div[1]/div[2]/form/div[2]/div/select")))
        select = Select(select_element)
        select.select_by_visible_text(company_name)

        button = driver.find_element(By.XPATH, "/html/body/div[1]/section[5]/div/div/div[1]/div[2]/form/div[3]/button")
        driver.execute_script("arguments[0].click();", button)

        address = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/section[2]/div/div[2]/div[4]"))).text.strip()
        product_manufactured = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div[3]/div[4]").text.strip()
        products = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div[4]/div[4]").text.strip()

        return {
            'Company Name': company_name,
            'Address': address,
            'Product Manufactured': product_manufactured,
            'Products': products,
        }
    except Exception as e:
        print(f"Failed to scrape {company_name}: {e}")
        return None

scraped_data = list(filter(None, map(scrape_company_data, company_names)))

df = pd.DataFrame(scraped_data)
print("\nScraped Data:\n", df)

driver.quit()

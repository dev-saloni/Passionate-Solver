from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get('https://acma.in/')
driver.implicitly_wait(5)

select_element = driver.find_element(By.XPATH, "/html/body/div[1]/section[5]/div/div/div[1]/div[2]/form/div[2]/div/select")
select = Select(select_element)
options_list = select.options[1:] 

data = []

for option in options_list:
    try:
        company_name = option.text.strip()
        print(f"Scraping: {company_name}")

        select.select_by_visible_text(company_name)

        driver.find_element(By.XPATH, "/html/body/div[1]/section[5]/div/div/div[1]/div[2]/form/div[3]/button").click()
        driver.implicitly_wait(2)

        address = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div[2]/div[4]").text.strip()
        product_manufactured = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div[3]/div[4]").text.strip()
        products = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div[4]/div[4]").text.strip()

        data.append({
            'Company Name': company_name,
            'Address': address,
            'Product Manufactured': product_manufactured,
            'Products': products,
        })

        driver.execute_script("window.history.go(-1)")
        driver.implicitly_wait(2)

        select_element = driver.find_element(By.XPATH, "/html/body/div[1]/section[5]/div/div/div[1]/div[2]/form/div[2]/div/select")
        select = Select(select_element)

    except Exception as e:
        print(f"Failed to scrape data for {company_name}: {e}")

df = pd.DataFrame(data)

print("\nScraped Data (Pandas DataFrame):\n")
print(df)

driver.quit()

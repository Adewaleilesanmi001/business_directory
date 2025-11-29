import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
import re


def chrome_driver():
    driver_path = ChromeDriverManager().install()
    print("Driver path:", driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security
    # Check if it's actually executable
    if not os.access(driver_path, os.X_OK):
        print("❌ Not executable. Trying to locate the real binary.")
        for root, dirs, files in os.walk(os.path.dirname(driver_path)):
            for file in files:
                if "chromedriver" in file and not file.endswith(".chromedriver"):
                    potential_path = os.path.join(root, file)
                    print("✅ Found likely candidate:", potential_path)
                    driver_path = potential_path
                    break

    return webdriver.Chrome(service=ChromeService(driver_path), options=options)


driver = chrome_driver()


company_names = []
company_web_addresses = []
company_contacts = []
company_emails = []

category = 'counselling'
url = f'https://ukbusinessportal.co.uk/category/{category}/'

responds = requests.get(url)
print(responds.status_code)



driver.get(url)
time.sleep(12)
source_code = driver.page_source

soup = BeautifulSoup(source_code, 'html.parser')

def scraping ():
    company_infos = soup.find_all('div', class_ = 'col-span-1 w-full flex items-center shadow-custom')
    for data in company_infos:

        try:
            company_name = data.find('h3', class_ = 'text-base md:text-lg xl:text-xl text-black hover:text-marine font-medium mb-2 mt-2 lg:mt-4').text.strip()
        except AttributeError:
            company_name = None
    
        try:
            company_web_address = data.find(class_="flex items-center gap-2 text-sm sm:text-xs lg:text-sm mb-1",href = re.compile("https")).text.strip().replace('https://', '').replace('www.', '').rstrip('/')
        except AttributeError:
            company_web_address = None
    
        try:
            company_contact = data.find(class_="flex items-center gap-2 text-sm sm:text-xs lg:text-sm mb-1",href = re.compile("tel")).text.strip().replace(' ', '')
        except AttributeError:
            company_contact = None

        try:
            company_email = data.find(class_="flex items-center gap-2 text-sm sm:text-xs lg:text-sm mb-1",href = re.compile("mailto")).text.strip()
        except AttributeError:
            company_email = None
            

        company_names.append(company_name)
        company_web_addresses.append(company_web_address)
        company_contacts.append(company_contact)
        company_emails.append(company_email)
        

    df = {
        'company_names' : company_names,
        'company_web_addresses': company_web_addresses,
        'company_contacts' : company_contacts,
        'company_emails' : company_emails
    }

    df = pd.DataFrame(df)
  
    df.to_csv(f'{category}.csv', index=False)
    print ( f'{category} added to csv')
    return df
    
    
print(scraping ())

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome WebDriver (Ensure you have downloaded ChromeDriver and its path is set)
# You can download ChromeDriver from: https://sites.google.com/a/chromium.org/chromedriver/downloads
driver = webdriver.Chrome()

# Define the URL for BookMyShow
BMS_url = "https://in.bookmyshow.com/explore/home"
driver.get(BMS_url )
time.sleep(20)
# Wait until the city selection element is present
#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sc-kaNhvL.jlISnX.ellipsis")))

# Click on the city selection dropdown
cities = driver.find_element(By.CLASS_NAME, "sc-kaNhvL.jlISnX.ellipsis")
cities.click()
time.sleep(2)

# Fetch all cities data
Cities_data = driver.find_elements(By.XPATH, '//span[@class="sc-iuDHTM uqCMs"]')

# Click on 'Other Cities' if needed
Other_Cities_tag = driver.find_element(By.CLASS_NAME, "sc-jxGEyO.fQHEXW")
Other_Cities_tag.click()
Other_Cities_data = driver.find_elements(By.XPATH, '//div[@class="sc-cqPOvA fmMura"]')

# Print all the cities retrieved
Cities = []
for e in Cities_data:
    Cities.append(e.get_attribute('innerHTML'))

print(Cities)

# Close the WebDriver session after scraping
driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the WebDriver
driver = webdriver.Chrome()  # Or use webdriver.Firefox() for Firefox

try:
    # Navigate to the website
    driver.get("https://upag.gov.in/dashboard/apy-overview-tab,apy-insights-cropwise-tab,apy-drilldown-tab?rtab=Area%2C+Production+%26+Yield&rtype=dashboards")

    # Wait for the page to load completely
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # Locate the table containing the data
    table = driver.find_element(By.TAG_NAME, "table")

    # Extract table headers
    headers = [header.text for header in table.find_elements(By.TAG_NAME, "th")]

    # Extract table rows
    rows = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:
            row_data = [cell.text for cell in cells]
            rows.append(row_data)

    # Create a DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Save the DataFrame to a CSV file
    df.to_csv("extracted_data.csv", index=False)

finally:
    # Close the WebDriver
    driver.quit()

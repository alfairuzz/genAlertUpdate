from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

url = "https://support.broadcom.com/web/ecx/security-advisory?segment=VC"

# Set up the WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

try:
    # Wait for the table to appear and have rows with data
    table_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#_securityadvisory_-root > div > div > div:nth-child(3) > div > div > div.card-body > div > div > table"))
    )
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#_securityadvisory_-root > div > div > div:nth-child(3) > div > div > div.card-body > div > div > table td"))
    )
    
    # Extract the table's HTML content
    table_html = table_element.get_attribute("outerHTML")

except Exception as e:
    print(f"Error: {e}")
    driver.quit()
    exit()

# Close the browser
driver.quit()

# Process the table HTML using BeautifulSoup
soup = BeautifulSoup(table_html, "html.parser")
table = soup.find("table")

# Extract data into a structured format
data = []
headers = [th.text.strip() for th in table.find_all("th")]
rows = table.find_all("tr")
for row in rows:
    cols = row.find_all("td")
    if cols:  # Only process rows with data
        data.append([col.text.strip() for col in cols])

# Convert to a DataFrame
if headers:
    df = pd.DataFrame(data, columns=headers)
else:
    df = pd.DataFrame(data)

# Save to a CSV file (optional)
df.to_csv("broadcom_security_advisory.csv", index=False)

print(df)
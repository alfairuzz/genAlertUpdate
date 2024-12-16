import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_oracle_updates():
    # URL for Oracle Security Alerts page
    url = "https://www.oracle.com/security-alerts/"

    # Make the GET request
    response = requests.get(url)

    # Get the HTML content
    html_content = response.content

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tables with the class 'otable-tech-basic otable-w2'
    tables = soup.find_all('table', class_='otable-tech-basic otable-w2')

    # Initialize an empty list to store data
    data = []

    # Loop through each table and extract the relevant data
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) >= 2:
                patch_update = columns[0].get_text(strip=True)
                url = columns[0].find('a')['href'] if columns[0].find('a') else None
                latest_version = columns[1].get_text(strip=True)
                data.append([patch_update, url, latest_version])

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=['Critical Patch Update', 'URL', 'Latest Version/Date'])


    df['Released Date'] = [i.split("-")[1] for i in df['Critical Patch Update']]

    # Output the DataFrame
    return df
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_paloalto_updates():
    url = "https://security.paloaltonetworks.com/rss.xml"

    # Fetch and parse the RSS feed
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")

    # Extract data
    data = []
    items = soup.find_all("item")

    data = []
    for item in items:
        title = item.find('title').get_text(strip=True) if item.find('title') else None
        pubDate = item.find('pubDate').get_text(strip=True) if item.find('pubDate') else None
        link = item.find('link').get_text(strip=True) if item.find('link') else None
        guid = item.find('guid').get_text(strip=True) if item.find('guid') else None
        
        data.append({
            'Title': title,
            'Published At': pubDate,
            'Link': link,
            'GUID': guid
        })

    df = pd.DataFrame(data)

    df['Published At'] = pd.to_datetime(df['Published At'], errors='coerce')
    df['Published At'] = df['Published At'].dt.strftime('%b %d, %Y')

    return df

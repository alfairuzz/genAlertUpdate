import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_solarwinds_updates():

    url = "https://www.solarwinds.com/shared-content/rss-feed/solarwinds-cve-rss-feed.xml"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")

    items = soup.find_all("item")

    records = []
    for item in items:
        guid = item.find("guid").get_text(strip=True) if item.find("guid") else None
        title = item.find("title").get_text(strip=True) if item.find("title") else None
        link = item.find("link").get_text(strip=True) if item.find("link") else None
        description = item.find("description").get_text(strip=True) if item.find("description") else None
        pubDate = item.find("pubDate").get_text(strip=True) if item.find("pubDate") else None

        # Parse and format the pubDate
        # The RSS date format is generally "Wed, 04 Dec 2024 00:00:00 GMT"
        # We convert this to datetime and then format it as requested, e.g. "Dec 10, 2024".
        if pubDate:
            pubDate_dt = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S %Z')
            formatted_pubDate = pubDate_dt.strftime('%b %d, %Y')
        else:
            formatted_pubDate = None

        records.append({
            "guid": guid,
            "title": title,
            "link": link,
            "description": description,
            "pubDate": formatted_pubDate
        })

    df = pd.DataFrame(records)
    
    return df
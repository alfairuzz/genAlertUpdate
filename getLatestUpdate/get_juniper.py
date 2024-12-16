import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd


def get_juniper_updates():
    url = "https://supportportal.juniper.net/s/global-search/%40uri?language=en_US#sort=relevancy&f:ctype=[Security%20Advisories]"
    selector = ".coveo-list-layout.CoveoResult"

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    time.sleep(10)  # Increase this if content takes longer to load

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    results = soup.select(selector)

    records = []
    for res in results:
        # Title and URL
        title_elem = res.select_one("a.CoveoResultLink")
        title = title_elem.get_text(strip=True) if title_elem else None
        link = title_elem['href'] if title_elem and title_elem.has_attr('href') else None

        # Publish Date
        # Look for the span that typically contains the date. Adjust this selector if needed.
        date_elem = res.select_one("span[data-field='@sfcec_community_publish_date_formula__c'] span")
        pub_date = date_elem.get_text(strip=True) if date_elem else None

        # Excerpt
        excerpt_elem = res.select_one("span.CoveoExcerpt")
        excerpt = excerpt_elem.get_text(strip=True) if excerpt_elem else None

        # Article Id
        # This may appear after a span with class coveo-field-caption and text "Article Id:"
        # The next span after that caption should contain the article id.
        article_id_elem = res.select_one("span[data-field='@sfcec_documentid__c'] span:not(.coveo-field-caption)")
        article_id = article_id_elem.get_text(strip=True) if article_id_elem else None

        records.append({
            "Title": title,
            "URL": link,
            "Publish Date": pub_date,
            "Excerpt": excerpt,
            "Article Id": article_id
        })

    df = pd.DataFrame(records)
    
    # Convert the 'Publish Date' column to datetime
    df['Publish Date'] = pd.to_datetime(df['Publish Date'], format='%Y-%m-%d', errors='coerce')
    
    df = df.sort_values(by = "Publish Date", ascending=False)

    # Now format it to "Dec 10, 2024" style
    df['Publish Date'] = df['Publish Date'].dt.strftime('%b %d, %Y')
    
    df = df.reset_index(drop=True)
    
    return df

import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_sap_updates():
    url = "https://support.sap.com/en/my-support/knowledge-base/security-notes-news.html?anchorId=section_370125364"
    selector = "#section_370125364 > div > div > div.rowWrapper.section > div > div.col-md-3.col-md-offset-0 > div > div > div > div.parsys > div > div"

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Select the container where the patch day notes are listed
        items = soup.select_one(selector)
        
        if items:
            data = []
            # Find all <a> tags within the selected items
            for a_tag in items.find_all('a'):
                title = a_tag.get('title', '').strip()
                url = a_tag.get('href', '').strip()
                date_text = a_tag.get_text(strip=True)

                # Append extracted data to the list
                data.append({
                    "Title": title,
                    "Date": date_text,
                    "URL": url
                })
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            base_url = "https://support.sap.com"
            
            df['URL'] = [base_url + i for i in df['URL']]
            
            return df
        
        else:
            print("No items found with the given selector.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
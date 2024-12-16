import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_wordpress_updates():
    url = "https://wordpress.org/news/category/releases/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <li> elements representing posts
        lis = soup.find_all('li', class_='wp-block-post')

        data = []
        for li in lis:
            # Extract version
            version_tag = li.select_one('.wp-block-wporg-release-version')
            version = version_tag.get_text(strip=True) if version_tag else None

            # Extract title and link
            title_tag = li.select_one('h2.wp-block-post-title a')
            title = title_tag.get_text(strip=True) if title_tag else None
            link = title_tag.get('href') if title_tag else None

            # Extract date (e.g., "November 21, 2024")
            date_tag = li.select_one('.wp-block-post-date time')
            date_str = date_tag.get_text(strip=True) if date_tag else None

            # Convert the date into "Dec 10, 2024" format
            # Assuming the original format is something like "November 21, 2024"
            # We parse with "%B %d, %Y" and then reformat to "%b %d, %Y"
            # which would produce "Nov 21, 2024"
            # If you want strictly "Dec 10, 2024" style (with that exact month),
            # it just means using the abbreviated month format.
            if date_str:
                parsed_date = datetime.strptime(date_str, "%B %d, %Y")
                date_converted = parsed_date.strftime("%b %d, %Y")  # e.g. "Nov 21, 2024"
            else:
                date_converted = None

            # Extract excerpt
            excerpt_tag = li.select_one('.wp-block-post-excerpt__excerpt')
            excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else None

            data.append({
                'Version': version,
                'Title': title,
                'Date': date_converted,
                'Link': link,
                'Excerpt': excerpt
            })

        df = pd.DataFrame(data)
        
        df = df[df['Title'].str.contains("Security Release")].reset_index(drop=True)
        
        return df
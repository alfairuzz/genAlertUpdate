import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_chrome_updates():
    # Get the first 100 results
    url = 'https://chromereleases.googleblog.com/search?max-results=100'

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the HTML content of the page
        #html_content = response.text
        
        # Get the HTML content
        html_content = response.content
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all paragraphs with the class 'gb-paragraph'
        headers = soup.find_all('div', class_='post')
        
        title_list = []
        link_list = []
        publish_date_list = []
        
        for item in headers:
            # Extract the title
            title = item.find('h2', class_='title').get_text(strip=True)

            # Extract the link
            link = item.find('h2', class_='title').find('a')['href']

            # Extract the publish date
            publish_date = item.find('span', class_='publishdate').get_text(strip=True)

            title_list.append(title)
            link_list.append(link)
            publish_date_list.append(publish_date)
            
        recent_ten_updates = {"Category": title_list,
                              "Publish Date": publish_date_list,
                              "Link": link_list}
        
        recent_ten_updates_df = pd.DataFrame(recent_ten_updates)
        
        # Get only "Stable Channel Update for Desktop" updates
        recent_ten_updates_filtered_df = recent_ten_updates_df[recent_ten_updates_df['Category'] == 'Stable Channel Update for Desktop'].reset_index(drop = True)
        
        # Convert the 'Date' column to the desired format
        recent_ten_updates_filtered_df['Publish Date'] = pd.to_datetime(recent_ten_updates_filtered_df['Publish Date'], format='%A, %B %d, %Y').dt.strftime('%b %d, %Y')
        
        return recent_ten_updates_filtered_df
        
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        
        

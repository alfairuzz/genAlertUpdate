import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_intel_updates():
    url = "https://www.intel.com/content/www/us/en/security-center/default.html"

    # Fetch and parse the RSS feed
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the HTML content of the page
        #html_content = response.text
        
        # Get the HTML content
        html_content = response.content
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Use the CSS selector to locate the table
        table = soup.select_one('#editorialTableBlade-1 > div > div:nth-child(2) > div.table-responsive > table')

        # Initialize lists to store table data
        advisories = []
        advisory_numbers = []
        updated_dates = []
        release_dates = []

        # Loop through table rows in tbody
        if table:
            for row in table.select('tbody > tr.data'):
                # Extract data from each column
                advisory = row.select_one('td:nth-child(1)').text.strip()
                advisory_number = row.select_one('td:nth-child(2)').text.strip()
                updated_date = row.select_one('td:nth-child(3)').text.strip()
                release_date = row.select_one('td:nth-child(4)').text.strip()
                
                # Append data to lists
                advisories.append(advisory)
                advisory_numbers.append(advisory_number)
                updated_dates.append(updated_date)
                release_dates.append(release_date)
        else:
            print("Table not found using the CSS selector")

        # Create a DataFrame from the extracted data
        df = pd.DataFrame({
            'Advisory': advisories,
            'Advisory Number': advisory_numbers,
            'Updated': updated_dates,
            'Release Date': release_dates
        })
        
        # Function to reformat date
        # Function to reformat date
        def reformat_date(date_str):
            for fmt in ('%B %d, %Y', '%b %d, %Y'):
                try:
                    # Attempt to parse with the current format
                    date_obj = datetime.strptime(date_str, fmt)
                    # Format the date as 'Dec 10, 2024'
                    return date_obj.strftime('%b %d, %Y')
                except ValueError:
                    pass
            # If none of the formats work, return the original string
            return date_str

        # Apply the function to 'Updated' and 'Release Date' columns
        df['Updated'] = df['Updated'].apply(reformat_date)
        df['Release Date'] = df['Release Date'].apply(reformat_date)


    return df
    
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_apple_updates():

    # URL of the webpage
    url = "https://support.apple.com/en-us/100100"

    # Send a GET request to fetch the HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text  # Get the HTML content
        soup = BeautifulSoup(html_content, "html.parser")  # Parse with BeautifulSoup
        
        # Use the CSS selector to find the desired table
        table = soup.select_one("#sections > div.table-wrapper.gb-table > table")
        
        if table:
            print("Table found!")
        else:
            print("Table not found with the given selector.")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        

    # Find the table
    table = soup.find("table", class_="gb-table")

    # Initialize data storage
    data = []

    # Loop through table rows
    for row in table.find_all("tr")[1:]:  # Skip the header row
        cols = row.find_all("td")
        if cols:  # Ensure it's not an empty row
            # Extract data from the columns
            name_info = cols[0].find("a").text if cols[0].find("a") else cols[0].text.strip()
            link = cols[0].find("a")["href"] if cols[0].find("a") else None
            available_for = cols[1].text.strip()
            release_date = cols[2].text.strip()

            # Append data to the list
            data.append({
                "Name and Info Link": name_info,
                "Link": link,
                "Available For": available_for,
                "Release Date": release_date
            })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    base_url = "https://support.apple.com"
    df['Link'] = [base_url + i if i is not None else i for i in df['Link']]

    # Convert date to "Dec 12, 2024" format
    df['Release Date'] = pd.to_datetime(df["Release Date"], errors='coerce').dt.strftime("%b %d, %Y")

    # Filter to only iOS/iPadOS/macOS
    include_list = ['iOS', 'iPadOS', 'macOS']

    # Filter the DataFrame
    df = df[df['Name and Info Link'].str.contains('|'.join(include_list), na=False)]
    
    
    return df.reset_index(drop=True)


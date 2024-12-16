from bs4 import BeautifulSoup
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_atlassian_updates():

    # URL and selector
    url = "https://www.atlassian.com/trust/security/advisories"
    css_selector = "#advisories > main > div:nth-child(4) > div > div.component.s0.between.component--block > div > div > div.column.column-md-6.s0.between"

    # Fetch the page content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
        print("HTML content fetched successfully!")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract the content using the CSS selector
    selected_content = soup.select_one(css_selector)

    # Display the extracted HTML
    if selected_content:
        print("Selected content extracted successfully!")
    else:
        print("No content found for the given CSS selector.")


    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all blocks
    blocks = soup.find_all("div", class_="component component--textblock")

    # Prepare data list
    data = []
    for block in blocks:
        try:
            month = block.find("h5").text.strip()  # Extract the month
            links = block.find_all("a")  # Extract all links
            for link in links:
                record = {
                    "Month": month,
                    "Title": link.text.strip(),
                    "Link": link['href']
                }
                data.append(record)
        except:
            continue

    # Create DataFrame
    df = pd.DataFrame(data)

    return df
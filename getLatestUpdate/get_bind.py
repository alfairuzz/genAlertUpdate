import subprocess
from bs4 import BeautifulSoup
import pandas as pd


def get_bind_updates():
    # Bind is a bit tricky becuase it has bot detection and protection so can't use requests library or selenium to extract (will get Error 403)
    # Thus, used Curl to request for the html content
    
    # URL to fetch
    url = "https://kb.isc.org/docs/aa-00913"

    # Curl command to fetch the content
    command = f"curl -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' '{url}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        html_content = result.stdout
        print("HTML content fetched successfully using curl!")
        
        # Use BeautifulSoup to parse the content
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Select content using the specific CSS selector
        selected_content = soup.select_one("#doc_content_block > div > div.content_container_text_sec.medium-layout > div > div.content_block_text > table:nth-child(8)")
        
        if selected_content:
            # Prettify and display the selected content
            prettified_content = selected_content.prettify()
        else:
            print("No content found for the given CSS selector.")
    else:
        print("Failed to fetch content using curl.")


    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the table
    table = soup.find("table")

    # Extract rows from the table
    rows = table.find_all("tr")

    # Prepare data for the DataFrame
    data = []
    for row in rows[1:]:  # Skip header row
        columns = row.find_all("td")
        data.append({
            "#": columns[0].text.strip(),
            "CVE Number": columns[1].find("a").text.strip(),
            "CVE Link": columns[1].find("a")["href"].strip(),
            "Short Description": columns[2].find("a").text.strip()
        })

    # Create the DataFrame
    df = pd.DataFrame(data)
    df['CVE Number'] = ["CVE-" + i for i in df['CVE Number']]
    
    return df

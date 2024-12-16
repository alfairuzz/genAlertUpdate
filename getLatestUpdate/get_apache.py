from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_apache_updates():

    # URL of the webpage
    url = "https://httpd.apache.org/security/vulnerabilities_24.html"

    # Fetch the HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text  # Extract HTML content as a string
        print("Apache content fetched successfully!")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")


    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract CVE details
    data = []
    for dt, dd in zip(soup.find_all("dt"), soup.find_all("dd")):
        cve_id = dt.find("a").text
        description = dd.find("p").text.strip()
        table = dd.find("table")
        rows = table.find_all("tr") if table else []
        
        details = {
            "CVE ID": cve_id,
            "Description": description,
            "Reported Date": "",
            "Fixed Date": "",
            "Update Release Date": "",
            "Affected Versions": "",
        }
        
        # Extract table rows
        for row in rows:
            header = row.find("td", class_="cve-header").text.strip()
            value = row.find("td", class_="cve-value").text.strip()
            if "Reported" in header:
                details["Reported Date"] = value
            elif "fixed" in header:
                details["Fixed Date"] = value
            elif "Update" in header:
                details["Update Release Date"] = value
            elif "Affects" in header:
                details["Affected Versions"] = value

        data.append(details)

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Convert date to "Dec 12, 2024" format
    df['Update Release Date'] = pd.to_datetime(df["Update Release Date"], errors='coerce').dt.strftime("%b %d, %Y")
    
    return df

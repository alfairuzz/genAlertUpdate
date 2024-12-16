import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_fortinet_updates():
    # Create a list to store the data
    data = []

    # Loop through the first 3 pages
    for page_number in range(1, 4):
        base_url = f"https://www.fortiguard.com/psirt?page={page_number}&date=&severity=&product=FortiClientMac,FortiNDR,FortiNAC,FortiWLC,FortiSIEM,FortiWAN,FortiADCManager,FortiSwitch,FortiDDoS-CM,FortiMail,FortiSandbox,FortiSwitchManager,FortiAP-U,FortiRecorder,FortiOS-6K7K,FortiAP-W2,FortiWeb,FortiClientAndroid,FortiAP-C,FortiAnalyzer,FortiAP-S,FortiDeceptor,FortiExtender,FortiEDR,FortiWLM,FortiProxy,FortiAuthenticator,FortiTester,FortiManager,FortiDDoS,FortiClientWindows,FortiDDoS-F,FortiClientiOS,FortiAnalyzer-BigData,FortiADC,FortiGuard,FortiWebManager,FortiVoiceEnterprise,FortiClientEMS,FortiOS,FortiSOAR,FortiAP,FortiClientLinux,FortiPortal&component=&version="

        # Make the GET request
        response = requests.get(base_url)

        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the container div
            div_content = soup.select_one("#full-page > section.table-body > div")
            
            if div_content:
                # Find all rows within the container div
                rows = div_content.find_all("div", class_="row")
                
                # Loop through each row and extract details
                for row in rows:
                    # Extract the advisory link from the "onclick" attribute
                    advisory_link = row.get("onclick", "").replace("location.href = '", "").replace("'", "").strip()
                    
                    # Extract title and CVE
                    title_div = row.find("div", class_="col-md-3")
                    title = title_div.find("b").get_text(strip=True) if title_div else "N/A"
                    try:
                        cve = title_div.find("b", class_="cve").get_text(strip=True) if title_div else "N/A"
                    except:
                        cve = "N/A"

                    # Extract description
                    description_divs = row.find_all("div", class_="col-md-3")
                    description_div = description_divs[1] if len(description_divs) > 1 else None
                    description = description_div.get_text(strip=True) if description_div else "N/A"

                    # Extract affected products and versions
                    products_versions = []
                    product_div = row.find("div", class_="col-md-2")
                    if product_div:
                        product_groups = product_div.find_all("span", class_="item-group")
                        for product_group in product_groups:
                            product_name = product_group.find("b").get_text(strip=True)
                            versions = product_group.find("span", class_="item-sub").get_text(strip=True)
                            products_versions.append(f"{product_name}: {versions}")

                    # Extract revised and published dates
                    date_div = row.find_all("div", class_="col d-none d-lg-block")
                    revised_on = (date_div[0].find("b").get_text(strip=True) if date_div else "N/A")
                    published_on = (date_div[0].find("small").get_text(strip=True).replace("Published:", "").strip() if date_div else "N/A")

                    # Extract severity. Get the second instance of the class being used
                    severity_divs = row.find_all("div", class_="col d-none d-lg-block text-center")
                    severity_div = severity_divs[1] if len(severity_divs) > 1 else None

                    severity = (
                        severity_div.find("b").get_text(strip=True)
                        if severity_div and severity_div.find("b")
                        else "N/A"
                    )

                    # Append extracted details to the data list
                    data.append({
                        "Advisory Link": advisory_link,
                        "Title": title,
                        "CVE": cve,
                        "Description": description,
                        "Affected Products and Versions": "; ".join(products_versions),
                        "Revised On": revised_on,
                        "Published On": published_on,
                        "Severity": severity
                    })
        else:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Convert the 'Published On' column to datetime for proper sorting
    df['Published On'] = pd.to_datetime(df['Published On'], format='%b %d, %Y')

    # Sort the DataFrame by the 'Published On' column in descending order
    df_sorted = df.sort_values(by='Published On', ascending=False)

    # Group by 'Published On' and count 'Advisory Link'
    grouped_df = (
        df_sorted.groupby(['Published On'])
        .count()[['Advisory Link']]
        .reset_index()
        .sort_values(by='Published On', ascending= False)
    )

    # Convert 'Published On' back to string format for display
    grouped_df['Published On'] = grouped_df['Published On'].dt.strftime('%b %d, %Y')
    df_sorted['Published On'] = df_sorted['Published On'].dt.strftime('%b %d, %Y')
    
    grouped_df = grouped_df.rename(columns = {"Advisory Link": "Advisories"})
    summary_df = grouped_df.head()
    
    df_sorted = df_sorted.reset_index(drop=True)
    
    return df_sorted



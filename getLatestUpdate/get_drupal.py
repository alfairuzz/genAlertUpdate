import pandas as pd
import requests
import xml.etree.ElementTree as ET


def get_drupal_updates():

    # Fetch the RSS feed
    url = "https://www.drupal.org/security/all/rss.xml"
    response = requests.get(url)
    root = ET.fromstring(response.content)

    # Extract relevant data from the RSS feed
    data = []
    for item in root.findall(".//item"):
        title = item.find("title").text if item.find("title") is not None else None
        link = item.find("link").text if item.find("link") is not None else None
        pub_date = item.find("pubDate").text if item.find("pubDate") is not None else None
        description = item.find("description").text if item.find("description") is not None else None

        # Split the title into components
        if title:
            title_parts = title.split(" - ")
            name = title_parts[0] if len(title_parts) > 0 else None
            criticality = title_parts[1] if len(title_parts) > 1 else None
            impact = title_parts[2] if len(title_parts) > 2 else None
            vul_id = title_parts[3] if len(title_parts) > 3 else None
        else:
            name, criticality, impact, vul_id = None, None, None, None

        data.append({
            "Title": name,
            "Criticality": criticality,
            "Impact": impact,
            "Vul ID": vul_id,
            "Link": link,
            "Publication Date": pub_date,
            "Description": description
        })

    # Convert the data into a DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame (if running interactively) or save to a file
    drupal_core_df = df[df['Title'].str.contains("Drupal core")].reset_index(drop=True)
    
    # Convert the 'Date' column to the desired format
    drupal_core_df['Publication Date'] = pd.to_datetime(
    drupal_core_df['Publication Date'], 
    format='%a, %d %b %Y %H:%M:%S %z'
    ).dt.strftime('%b %d, %Y')

    return drupal_core_df

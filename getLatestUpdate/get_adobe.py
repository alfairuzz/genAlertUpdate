import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime



def get_adobe_updates():
    """Extracts the update table for Adobe Acrobat Reader and Adobe Experience Manager

    Returns:
        Dataframes: df_reader, df_manager
    """
    
    # URL
    url = "https://helpx.adobe.com/security/security-bulletin.html#experience-manager"

    # CSS Selectors
    css_selector_manager = "#root_content_flex_items_position > div > div:nth-child(88) > div > table"
    css_selector_reader = "#root_content_flex_items_position > div > div:nth-child(206) > div > table"

    # Fetch the webpage
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        def extract_table_data(css_selector):
            table = soup.select_one(css_selector)
            if table:
                rows = table.find_all("tr")
                data = []
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) > 0:
                        # Extract link from the first cell
                        link_tag = cells[0].find("a")
                        link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else None
                        
                        # Extract other columns
                        row_data = [cell.get_text(strip=True) for cell in cells]
                        row_data.append(link)  # Append the link to the row data
                        data.append(row_data)
                
                # Define column names (including the "Link" column)
                columns = ["Bulletin", "Release Date", "Last Updated", "Link"]
                return pd.DataFrame(data, columns=columns)
            else:
                print(f"Table not found for selector: {css_selector}")
                return None
            
        def convert_dates(df):
            # Convert dates to a uniform "Dec 12, 2024" format
            df["Release Date"] = pd.to_datetime(df["Release Date"], errors='coerce').dt.strftime("%b %d, %Y")
            df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors='coerce').dt.strftime("%b %d, %Y")
            
            return df
        
        def full_site_link(df):
            base_url = "https://helpx.adobe.com"
            df['Link'] = [base_url + i for i in df['Link']]
            
            return df
        
        # Extract data for Adobe Experience Manager
        df_manager = extract_table_data(css_selector_manager)
        if df_manager is not None:
            df_manager = convert_dates(df_manager)
            df_manager = full_site_link(df_manager)
            
            print("Adobe Experience Manager extracted.")
        
        # Extract data for Adobe Acrobat/Reader
        df_reader = extract_table_data(css_selector_reader)
        if df_reader is not None:
            # convert dates into "Dec 12, 2024" format
            df_reader = convert_dates(df_reader)
            df_reader = full_site_link(df_reader)
            
            print("Adobe Acrobat/Reader extracted")
            

    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        
    return df_reader, df_manager


def get_adobe_latest_publication(d1, d2):
    date1_obj = datetime.strptime(d1, "%b %d, %Y")
    date2_obj = datetime.strptime(d2, "%b %d, %Y")

    # Compare dates
    if date1_obj > date2_obj:
        latest_date = d1
    else:
        latest_date = d2
        
    return latest_date

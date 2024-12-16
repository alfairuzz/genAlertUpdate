import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime



def get_joomla_updates():

    url = "https://developer.joomla.org/security-centre.html"

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the HTML content
        html_content = response.content
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # This selects the main container holding the items
        table = soup.select_one("#content > div.com-content-category-blog.blog > div.com-content-category-blog__items.blog-items")
        
        # Each security announcement is in a div with class 'com-content-category-blog__item blog-item'
        items = table.select("div.com-content-category-blog__item.blog-item")
        
        records = []
        for item in items:
            data = {}
            
            # Title
            title_elem = item.select_one(".page-header h2 a")
            data["Title"] = title_elem.get_text(strip=True) if title_elem else None
            
            # Get the <ul> that contains the info fields
            info_list = item.select_one("div.item-content > ul")
            if info_list:
                # Create a map for known fields
                fields_map = {
                    'Project:': 'Project',
                    'SubProject:': 'SubProject',
                    'Impact:': 'Impact',
                    'Severity:': 'Severity',
                    'Probability:': 'Probability',
                    'Versions:': 'Versions',
                    'Exploit type:': 'Exploit Type',
                    'Reported Date:': 'Reported Date',
                    'Fixed Date:': 'Fixed Date',
                    'CVE Number:': 'CVE Number'
                }
                
                for li in info_list.select("li"):
                    strong_tag = li.select_one("strong")
                    if strong_tag:
                        field_name = strong_tag.get_text(strip=True)
                        # Extract text after the strong tag
                        value = li.get_text(strip=True).replace(field_name, '').strip().strip(':')
                        if field_name in fields_map:
                            data[fields_map[field_name]] = value
                            
            # Description
            description_header = item.find("h3", text="Description")
            if description_header:
                # The description text might be in the next sibling div
                desc_div = description_header.find_next_sibling("div")
                data["Description"] = desc_div.get_text(strip=True) if desc_div else None
            
            # Affected Installs
            affected_header = item.find("h3", text="Affected Installs")
            if affected_header:
                affected_div = affected_header.find_next_sibling("p")
                data["Affected Installs"] = affected_div.get_text(strip=True) if affected_div else None
            
            # Solution
            solution_header = item.find("h3", text="Solution")
            if solution_header:
                solution_p = solution_header.find_next_sibling("p")
                data["Solution"] = solution_p.get_text(strip=True) if solution_p else None
            
            # Contact
            contact_header = item.find("h3", text="Contact")
            if contact_header:
                contact_p = contact_header.find_next_sibling("p")
                data["Contact"] = contact_p.get_text(strip=True) if contact_p else None
            
            # Reported By
            reported_by_div = item.select_one("div.alert.alert-info")
            if reported_by_div:
                # The text after "Reported By:" can be extracted
                reported_by_text = reported_by_div.get_text(strip=True)
                # The line typically starts with "Reported By:"
                if "Reported By:" in reported_by_text:
                    data["Reported By"] = reported_by_text.replace("Reported By:", "").strip()
                else:
                    data["Reported By"] = reported_by_text
            
            records.append(data)
        
        # Create DataFrame from the records
        df = pd.DataFrame(records)
        
        # Convert the 'Fixed Date' column to datetime and then reformat it
        if 'Fixed Date' in df.columns:
            # First, parse the date assuming it is in YYYY-MM-DD format
            df['Fixed Date'] = pd.to_datetime(df['Fixed Date'], format='%Y-%m-%d', errors='coerce')
            
            # Now format it to "Dec 10, 2024" style (short month name, day, year)
            df['Fixed Date'] = df['Fixed Date'].dt.strftime('%b %d, %Y')
            
        return df
            
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
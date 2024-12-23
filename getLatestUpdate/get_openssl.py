import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_openssl_updates():

    url = "https://openssl-library.org/news/vulnerabilities/index.html"
    selector = "#content > article"

    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Select the main article where vulnerabilities are listed
        article = soup.select_one(selector)
        if not article:
            print("No article found with the given selector.")
        else:
            vulns = []
            # Each vulnerability is represented by <h4 id="CVE-..."> followed by a <dl>
            for h4 in article.select('h3[id^="CVE-"]'):
                cve_id = h4.get('id')
                title_elem = h4.find('a')
                cve_link = title_elem.get('href') if title_elem else None
                cve_title = title_elem.get_text(strip=True) if title_elem else None
                
                dl = h4.find_next('dl')
                if not dl:
                    continue
                
                details = {}
                dts = dl.find_all('dt')
                dds = dl.find_all('dd')
                
                # Pair up dt and dd text
                for dt, dd in zip(dts, dds):
                    dt_text = dt.get_text(strip=True)
                    dd_text = dd.get_text(strip=True)
                    details[dt_text] = dd_text
                
                # Extract references (if any)
                references = []
                for dt in dts:
                    if 'References' in dt.get_text(strip=True):
                        references_dd = dt.find_next('dd')
                        if references_dd:
                            ref_links = references_dd.find_all('a', href=True)
                            for ref_link in ref_links:
                                references.append((ref_link.get_text(strip=True), ref_link['href']))
                
                affected_versions = details.get('Affected', None)
                published_at = details.get('Published at', None)
                found_by = details.get('Found by', None)
                severity = details.get('Severity', None)
                
                vulns.append({
                    'CVE': cve_id,
                    'Title': cve_title,
                    'Severity': severity,
                    'Found by': found_by,
                    'Published at': published_at,
                    'Affected': affected_versions,
                    'References': references
                })
            
            df = pd.DataFrame(vulns)
            df['Published at'] = pd.to_datetime(df['Published at'], format='%d %B %Y', errors='coerce')
            df['Published at'] = df['Published at'].dt.strftime('%b %d, %Y')
            
            return df
            
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
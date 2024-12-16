import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_samba_updates():
    url = "https://www.samba.org/samba/history/security.html"
    selector = "#main > table"

    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Select the main article where vulnerabilities are listed
        table = soup.select_one(selector)
        
        rows = table.find_all("tr")[1:]  # skip the header row(s)

        data = []
        for tr in rows:
            # Extract all <td> cells in the row
            tds = tr.find_all("td")
            if len(tds) < 6:
                # Some rows might be empty or header-like, skip them
                continue

            # Extract text and clean it up
            date_issued = tds[0].get_text(strip=True)
            download = " ".join([a.get_text(strip=True) for a in tds[1].find_all("a")]) if tds[1].find("a") else tds[1].get_text(strip=True)
            known_issues = tds[2].get_text(" ", strip=True)  # join by space to prevent newline merges
            affected_releases = tds[3].get_text(strip=True)
            cve_links = tds[4].find_all("a")
            cves = ", ".join(a.get_text(strip=True) for a in cve_links) if cve_links else tds[4].get_text(strip=True)
            details_links = tds[5].find_all("a")
            details = ", ".join(a.get_text(strip=True) for a in details_links) if details_links else tds[5].get_text(strip=True)

            # Append row of data
            data.append({
                "Date Issued": date_issued,
                "Download": download,
                "Known Issue(s)": known_issues,
                "Affected Releases": affected_releases,
                "CVE ID #": cves,
                "Details": details
            })

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=["Date Issued", "Download", "Known Issue(s)", "Affected Releases", "CVE ID #", "Details"])
        def format_date(d):
            try:
                parsed = datetime.strptime(d, "%d %B %Y")
                return parsed.strftime("%b %d, %Y")
            except ValueError:
                # If formatting fails, return the original string
                return d

        df["Date Issued"] = df["Date Issued"].apply(format_date)
        
        # Show the resulting DataFrame
        return df
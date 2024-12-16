import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_gitlab_updates():
    """Use to get the various GitLab releases for users to select.
    """
    # URL for GitLab security releases RSS feed
    url = "https://about.gitlab.com/security-releases.xml"

    # Fetch and parse the RSS feed
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")

    # Extract data
    data = []
    entries = soup.find_all("entry")

    for entry in entries:
        title = entry.find("title").text
        link = entry.find("link")["href"]
        published = entry.find("published").text
        author = entry.find("author").find("name").text

        # Extract vulnerabilities table
        content = entry.find("content").text
        content_soup = BeautifulSoup(content, "html.parser")
        table = content_soup.find("table")

        if table:
            rows = table.find_all("tr")
            for row in rows[1:]:  # Skip the header row
                cells = row.find_all("td")
                vuln_title = cells[0].get_text(strip=True)
                severity = cells[1].get_text(strip=True)
                data.append({
                    "Title": title,
                    "Link": link,
                    "Published Date": published,
                    "Author": author,
                    "Vulnerability Title": vuln_title,
                    "Severity": severity
                })

    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Create Summary Table
    df['Published Date (raw)'] = pd.to_datetime(df['Published Date']).dt.strftime('%Y-%m-%d')
    df['Published Date'] = pd.to_datetime(df['Published Date (raw)']).dt.strftime('%b %d, %Y')

    summary_table = (df.groupby(['Title', 'Published Date (raw)', 'Published Date', "Link"])
        .agg(Vulnerabilities=('Title', 'count'))
    ).sort_values(by = "Published Date (raw)", ascending=False).reset_index().head()
    
    # When displaying the table out, hide the link column
    return summary_table


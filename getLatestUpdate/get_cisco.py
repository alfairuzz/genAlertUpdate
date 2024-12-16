import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_cisco_updates():
    # Returns 2 output, (1) Detailed Info, (2) Summary Table
    
    # Get the first 50 results
    url = 'https://sec.cloudapps.cisco.com/security/center/publicationService.x?criteria=exact&cves=&keyword=&last_published_date=&limit=50&offset=0&publicationTypeIDs=1,3&securityImpactRatings=&sort=-day_sir&title='

    # Make the GET request
    response = requests.get(url)

    data = response.json()

    """_summary_
        ciscoBugId: "CSCwj10299"
        cve: "CVE-2024-20432"
        cwe: "CWE-77"
        firstPublished: "2024-10-02T16:00:00.000+0000"
        id: 1
        identifier: "cisco-sa-ndfc-cmdinj-UvYZrKfr"
        lastPublished: "2024-10-02T16:00:00.000+0000"
        name: "Cisco Security Advisory"
        relatedResource: []
        severity: "Critical"
        status: "New"
        summary: "A vulnerability in the REST API and web UI of Cisco Nexus Dashboard Fabric Controller (NDFC) could allow an authenticated, low-privileged, remote attacker to perform a command injection attack against an affected device.&nbsp;This vulnerability is due to improper "
        title: "Cisco Nexus Dashboard Fabric Controller Arbitrary Command Execution Vulnerability"
        totalCount : 4946
        url: "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ndfc-cmdinj-UvYZrKfr"
        version: "1.0"
        workarounds: "No"
        workflowStatus: 
        null

    """
    cisco_summary_table_df = pd.DataFrame(data = {
        "Advisory": [],
        "Severity": [],
        "CVE": [],
        "Last Updated": [],
        "Version": [],
        "Status": [],
        "Summary": [],
        'Link': [],
        })

    for item in data:
        advisory = item['title']
        severity = item['severity']
        cve = item['cve']
        last_updated = item['lastPublished']
        version = item['version']
        status = item['status']
        summary = item['summary']
        url_link = item['url']
        
        data = {"Advisory": [advisory],
                "Severity": [severity],
                "CVE": [cve],
                "Last Updated": [last_updated],
                "Version": [version],
                "Status": [status],
                "Summary": [summary],
                'Link': [url_link],
                }
        
        temp_df = pd.DataFrame(data)
        cisco_summary_table_df = pd.concat([cisco_summary_table_df, temp_df], ignore_index=True)

    # I only want those that are version = "1.0"
    filtered_cisco_summary_table_df = cisco_summary_table_df[cisco_summary_table_df['Version'] == "1.0"]

    # Convert 'Last Updated' to a date format using .loc[] to avoid SettingWithCopyWarning
    filtered_cisco_summary_table_df.loc[:, 'Last Updated'] = pd.to_datetime(filtered_cisco_summary_table_df['Last Updated']).dt.date

    filtered_cisco_summary_table_df = filtered_cisco_summary_table_df.reset_index(drop = True)

    # Convert the 'Date' column to the desired format
    filtered_cisco_summary_table_df['Last Updated'] = pd.to_datetime(filtered_cisco_summary_table_df['Last Updated'], format='%A, %B %d, %Y').dt.strftime('%b %d, %Y')

    return filtered_cisco_summary_table_df

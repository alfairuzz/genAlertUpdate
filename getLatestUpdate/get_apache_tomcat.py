from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_apache_tomcat_8_updates():
    
    # URL of the webpage
    url = "https://tomcat.apache.org/security-8.html"

    # Fetch the HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text  # Extract HTML content as a string
        print("Apache Tomcat 8 content fetched successfully!")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract details
    data = []
    sections = soup.find_all("div", class_="text")

    for section in sections:
        # Find the preceding <h3> for the current <div>
        previous_h3 = section.find_previous("h3")
        if previous_h3:
            fixed_version = previous_h3.text.strip()
            release_date = previous_h3.find("span", class_="pull-right").text.strip() if previous_h3.find("span", class_="pull-right") else None
        else:
            fixed_version = None
            release_date = None

        cve_info = {}
        paragraphs = section.find_all("p")
        for paragraph in paragraphs:
            try:
                if "CVE" in paragraph.text and paragraph.find("a"):
                    if cve_info:  # Append previous CVE data to the list before starting a new one
                        cve_info["Fixed Version"] = fixed_version
                        cve_info["Release Date"] = release_date
                        data.append(cve_info)
                    cve_info = {
                        "Severity": paragraph.text.split(":")[1].strip(),
                        "CVE ID": paragraph.find("a").text,
                        "CVE Link": paragraph.find("a")["href"],
                        "Description": "",
                        "Commit": "",
                        "Reported Date": "",
                        "Public Date": "",
                        "Affected Versions": "",
                        "Fixed Version": fixed_version,
                        "Release Date": release_date
                    }
                elif "fixed with commit" in paragraph.text and cve_info:
                    cve_info["Commit"] = paragraph.find("a")["href"]
                elif "reported to" in paragraph.text or "identified by" in paragraph.text:
                    text = paragraph.text
                    cve_info["Reported Date"] = text.split("on")[1].split(".")[0].strip()
                    cve_info["Public Date"] = text.split("public on")[1].strip() if "public on" in text else ""
                elif "Affects:" in paragraph.text and cve_info:
                    cve_info["Affected Versions"] = paragraph.text.split("Affects:")[1].strip()
                elif cve_info:
                    cve_info["Description"] += paragraph.text.strip() + " "
            except (KeyError, IndexError, AttributeError):
                # Ignore sections that cause errors
                continue

        # Append the last CVE entry for the section
        if cve_info:
            cve_info["Fixed Version"] = fixed_version
            cve_info["Release Date"] = release_date
            data.append(cve_info)

    # Create DataFrame
    df = pd.DataFrame(data)

    df = df.drop(columns = "Severity")

    df['Release Date'] = pd.to_datetime(df["Release Date"], errors='coerce').dt.strftime("%b %d, %Y")

    return df


def get_apache_tomcat_9_updates():
    
    # URL of the webpage
    url = "https://tomcat.apache.org/security-9.html"

    # Fetch the HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text  # Extract HTML content as a string
        print("Apache Tomcat 9 content fetched successfully!")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract details
    data = []
    sections = soup.find_all("div", class_="text")

    for section in sections:
        # Find the preceding <h3> for the current <div>
        previous_h3 = section.find_previous("h3")
        if previous_h3:
            fixed_version = previous_h3.text.strip()
            release_date = previous_h3.find("span", class_="pull-right").text.strip() if previous_h3.find("span", class_="pull-right") else None
        else:
            fixed_version = None
            release_date = None

        cve_info = {}
        paragraphs = section.find_all("p")
        for paragraph in paragraphs:
            try:
                if "CVE" in paragraph.text and paragraph.find("a"):
                    if cve_info:  # Append previous CVE data to the list before starting a new one
                        cve_info["Fixed Version"] = fixed_version
                        cve_info["Release Date"] = release_date
                        data.append(cve_info)
                    cve_info = {
                        "Severity": paragraph.text.split(":")[1].strip(),
                        "CVE ID": paragraph.find("a").text,
                        "CVE Link": paragraph.find("a")["href"],
                        "Description": "",
                        "Commit": "",
                        "Reported Date": "",
                        "Public Date": "",
                        "Affected Versions": "",
                        "Fixed Version": fixed_version,
                        "Release Date": release_date
                    }
                elif "fixed with commit" in paragraph.text and cve_info:
                    cve_info["Commit"] = paragraph.find("a")["href"]
                elif "reported to" in paragraph.text or "identified by" in paragraph.text:
                    text = paragraph.text
                    cve_info["Reported Date"] = text.split("on")[1].split(".")[0].strip()
                    cve_info["Public Date"] = text.split("public on")[1].strip() if "public on" in text else ""
                elif "Affects:" in paragraph.text and cve_info:
                    cve_info["Affected Versions"] = paragraph.text.split("Affects:")[1].strip()
                elif cve_info:
                    cve_info["Description"] += paragraph.text.strip() + " "
            except (KeyError, IndexError, AttributeError):
                # Ignore sections that cause errors
                continue

        # Append the last CVE entry for the section
        if cve_info:
            cve_info["Fixed Version"] = fixed_version
            cve_info["Release Date"] = release_date
            data.append(cve_info)

    # Create DataFrame
    df = pd.DataFrame(data)

    df = df.drop(columns = "Severity")

    df['Release Date'] = pd.to_datetime(df["Release Date"], errors='coerce').dt.strftime("%b %d, %Y")

    return df


def get_apache_tomcat_10_updates():
    
    # URL of the webpage
    url = "https://tomcat.apache.org/security-10.html"

    # Fetch the HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text  # Extract HTML content as a string
        print("Apache Tomcat 10 content fetched successfully!")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract details
    data = []
    sections = soup.find_all("div", class_="text")

    for section in sections:
        # Find the preceding <h3> for the current <div>
        previous_h3 = section.find_previous("h3")
        if previous_h3:
            fixed_version = previous_h3.text.strip()
            release_date = previous_h3.find("span", class_="pull-right").text.strip() if previous_h3.find("span", class_="pull-right") else None
        else:
            fixed_version = None
            release_date = None

        cve_info = {}
        paragraphs = section.find_all("p")
        for paragraph in paragraphs:
            try:
                if "CVE" in paragraph.text and paragraph.find("a"):
                    if cve_info:  # Append previous CVE data to the list before starting a new one
                        cve_info["Fixed Version"] = fixed_version
                        cve_info["Release Date"] = release_date
                        data.append(cve_info)
                    cve_info = {
                        "Severity": paragraph.text.split(":")[1].strip(),
                        "CVE ID": paragraph.find("a").text,
                        "CVE Link": paragraph.find("a")["href"],
                        "Description": "",
                        "Commit": "",
                        "Reported Date": "",
                        "Public Date": "",
                        "Affected Versions": "",
                        "Fixed Version": fixed_version,
                        "Release Date": release_date
                    }
                elif "fixed with commit" in paragraph.text and cve_info:
                    cve_info["Commit"] = paragraph.find("a")["href"]
                elif "reported to" in paragraph.text or "identified by" in paragraph.text:
                    text = paragraph.text
                    cve_info["Reported Date"] = text.split("on")[1].split(".")[0].strip()
                    cve_info["Public Date"] = text.split("public on")[1].strip() if "public on" in text else ""
                elif "Affects:" in paragraph.text and cve_info:
                    cve_info["Affected Versions"] = paragraph.text.split("Affects:")[1].strip()
                elif cve_info:
                    cve_info["Description"] += paragraph.text.strip() + " "
            except (KeyError, IndexError, AttributeError):
                # Ignore sections that cause errors
                continue

        # Append the last CVE entry for the section
        if cve_info:
            cve_info["Fixed Version"] = fixed_version
            cve_info["Release Date"] = release_date
            data.append(cve_info)

    # Create DataFrame
    df = pd.DataFrame(data)

    df = df.drop(columns = "Severity")

    df['Release Date'] = pd.to_datetime(df["Release Date"], errors='coerce').dt.strftime("%b %d, %Y")

    return df


def get_apache_tomcat_11_updates():
    
    # URL of the webpage
    url = "https://tomcat.apache.org/security-11.html"

    # Fetch the HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text  # Extract HTML content as a string
        print("Apache Tomcat 11 content fetched successfully!")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract details
    data = []
    sections = soup.find_all("div", class_="text")

    for section in sections:
        # Find the preceding <h3> for the current <div>
        previous_h3 = section.find_previous("h3")
        if previous_h3:
            fixed_version = previous_h3.text.strip()
            release_date = previous_h3.find("span", class_="pull-right").text.strip() if previous_h3.find("span", class_="pull-right") else None
        else:
            fixed_version = None
            release_date = None

        cve_info = {}
        paragraphs = section.find_all("p")
        for paragraph in paragraphs:
            try:
                if "CVE" in paragraph.text and paragraph.find("a"):
                    if cve_info:  # Append previous CVE data to the list before starting a new one
                        cve_info["Fixed Version"] = fixed_version
                        cve_info["Release Date"] = release_date
                        data.append(cve_info)
                    cve_info = {
                        "Severity": paragraph.text.split(":")[1].strip(),
                        "CVE ID": paragraph.find("a").text,
                        "CVE Link": paragraph.find("a")["href"],
                        "Description": "",
                        "Commit": "",
                        "Reported Date": "",
                        "Public Date": "",
                        "Affected Versions": "",
                        "Fixed Version": fixed_version,
                        "Release Date": release_date
                    }
                elif "fixed with commit" in paragraph.text and cve_info:
                    cve_info["Commit"] = paragraph.find("a")["href"]
                elif "reported to" in paragraph.text or "identified by" in paragraph.text:
                    text = paragraph.text
                    cve_info["Reported Date"] = text.split("on")[1].split(".")[0].strip()
                    cve_info["Public Date"] = text.split("public on")[1].strip() if "public on" in text else ""
                elif "Affects:" in paragraph.text and cve_info:
                    cve_info["Affected Versions"] = paragraph.text.split("Affects:")[1].strip()
                elif cve_info:
                    cve_info["Description"] += paragraph.text.strip() + " "
            except (KeyError, IndexError, AttributeError):
                # Ignore sections that cause errors
                continue

        # Append the last CVE entry for the section
        if cve_info:
            cve_info["Fixed Version"] = fixed_version
            cve_info["Release Date"] = release_date
            data.append(cve_info)

    # Create DataFrame
    df = pd.DataFrame(data)

    df = df.drop(columns = "Severity")

    df['Release Date'] = pd.to_datetime(df["Release Date"], errors='coerce').dt.strftime("%b %d, %Y")

    return df

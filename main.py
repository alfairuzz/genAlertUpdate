import streamlit as st
import time
import pandas as pd
import io
import xlsxwriter
from datetime import datetime

from getLatestUpdate.get_adobe import get_adobe_updates, get_adobe_latest_publication
from getLatestUpdate.get_apache import get_apache_updates
from getLatestUpdate.get_apache_tomcat import (get_apache_tomcat_8_updates, 
                                               get_apache_tomcat_9_updates,
                                               get_apache_tomcat_10_updates, 
                                               get_apache_tomcat_11_updates)
from getLatestUpdate.get_apple import get_apple_updates
from getLatestUpdate.get_atlassian import get_atlassian_updates
from getLatestUpdate.get_bind import get_bind_updates
# reserved for VMWare
from getLatestUpdate.get_chrome import get_chrome_updates
from getLatestUpdate.get_cisco import get_cisco_updates
from getLatestUpdate.get_drupal import get_drupal_updates
from getLatestUpdate.get_fortinet import get_fortinet_updates
from getLatestUpdate.get_gitlab import get_gitlab_updates
from getLatestUpdate.get_intel import get_intel_updates
from getLatestUpdate.get_joomla import get_joomla_updates
from getLatestUpdate.get_juniper import get_juniper_updates
from getLatestUpdate.get_microsoft import get_microsoft_updates
from getLatestUpdate.get_openssl import get_openssl_updates
from getLatestUpdate.get_oracle import get_oracle_updates
from getLatestUpdate.get_paloalto import get_paloalto_updates
from getLatestUpdate.get_samba import get_samba_updates
from getLatestUpdate.get_sap import get_sap_updates
from getLatestUpdate.get_solarwinds import get_solarwinds_updates
from getLatestUpdate.get_wordpress import get_wordpress_updates


# ====== START: Side Bar Details ======
with st.sidebar:
    st.markdown(
        "<h1 style='font-size:28px;'>🚀 Usage</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "Start by clicking on the check for updates button on the right."
    )
    st.markdown(
        "The application will then extract and summarise the "
        "relevant information into a downloadable .xlsx file."
    )

# ====== END: Side Bar Details ======

# ====== START: Main Page Header ======
st.markdown(
    "<h1>🧹 Web Scraper UI "
    "<small style='font-size: 12px;'>by C.O</small></h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "This application is designed to extract key vulnerability details, "
    "including CVE information, affected products, and CVE base scores, from "
    "specified product websites. This tool simplifies the process of gathering "
    "security-related data for analysis."
)

# Get today's date and format it
today_date = datetime.now().strftime('%b, %d, %Y')

st.markdown("----")

# ====== END: Main Page Header ======

# ====== START: Session State Initialisation ======

# Define the key session states
if "check_status" not in st.session_state:
    st.session_state.check_status = False
    
if "extraction_status" not in st.session_state:
    st.session_state.extraction_status = False

if "adobe_latest_publication" not in st.session_state: # to store latest release date
    st.session_state.adobe_latest_publication = ""
    
if "apache_latest_publication" not in st.session_state: # to store latest release date
    st.session_state.apache_latest_publication = ""
    
if "apache_tomcat_8_latest_publication" not in st.session_state:
    st.session_state.apache_tomcat_8_latest_publication = ""
    
if "apache_tomcat_9_latest_publication" not in st.session_state:
    st.session_state.apache_tomcat_9_latest_publication = ""
    
if "apache_tomcat_10_latest_publication" not in st.session_state:
    st.session_state.apache_tomcat_10_latest_publication = ""
    
if "apache_tomcat_11_latest_publication" not in st.session_state:
    st.session_state.apache_tomcat_11_latest_publication = ""
    
if "apple_latest_publication" not in st.session_state:
    st.session_state.apple_latest_publication = ""
    
if "atlassian_latest_publication" not in st.session_state:
    st.session_state.atlassian_latest_publication = ""
    
if "bind_latest_publication" not in st.session_state:
    st.session_state.bind_latest_publication = ""
    
if "chrome_latest_publication" not in st.session_state:
    st.session_state.chrome_latest_publication = ""
    
if "cisco_latest_publication" not in st.session_state:
    st.session_state.cisco_latest_publication = ""

if "drupal_latest_publication" not in st.session_state:
    st.session_state.drupal_latest_publication = ""

if "fortinet_latest_publication" not in st.session_state:
    st.session_state.fortinet_latest_publication = ""
    
if "gitlab_latest_publication" not in st.session_state:
    st.session_state.gitlab_latest_publication = ""
    
if "intel_latest_publication" not in st.session_state:
    st.session_state.intel_latest_publication = ""

if "joomla_latest_publication" not in st.session_state:
    st.session_state.joomla_latest_publication = ""
    
if "juniper_latest_publication" not in st.session_state:
    st.session_state.juniper_latest_publication = ""
    
if "microsoft_latest_publication" not in st.session_state:
    st.session_state.microsoft_latest_publication = ""
    
if "openssl_latest_publication" not in st.session_state:
    st.session_state.openssl_latest_publication = ""
    
if "oracle_latest_publication" not in st.session_state:
    st.session_state.oracle_latest_publication = ""
    
if "paloalto_latest_publication" not in st.session_state:
    st.session_state.paloalto_latest_publication = ""
    
if "samba_latest_publication" not in st.session_state:
    st.session_state.samba_latest_publication = ""
    
if "sap_latest_publication" not in st.session_state:
    st.session_state.sap_latest_publication = ""
    
if "solarwinds_latest_publication" not in st.session_state:
    st.session_state.solarwinds_latest_publication = ""
    
if "wordpress_latest_publication" not in st.session_state:
    st.session_state.wordpress_latest_publication = ""
    
# ====== END: Session State Initialisation ======
    
def convert_df(df):
    # Use a BytesIO buffer to store the Excel file in memory
    output = io.BytesIO()
    
    # Write the DataFrame to the buffer. Can also include more than one sheet.
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        
    # Get the binary content of the buffer
    return output.getvalue()

    
def export_vulnerabilities(df_list):
    data = {
        "Product": ["Product A", "Product B", "Product C"],
        "Rating": [4.5, 3.8, 4.9],
        "Category": ["Electronics", "Home", "Office"]
    }

    df = pd.DataFrame(data)
    excel = convert_df(df)

    return excel


def retrieve_latest_vulnerability_updates():
    
    
    # ====== START: Check for Update Logic ======
    button_placeholder = st.empty()  # Placeholder for the button
    
    if not st.session_state.check_status:
        if button_placeholder.button("Check for updates"):
            st.sidebar.markdown("---")
            
            # Simulating update checks
            with st.sidebar.status("Checking for updates ...", expanded=True) as status:
                
                # Product 1
                st.write("Searching for Adobe...")
                adobe_reader_df, adobe_exp_manager_df = get_adobe_updates()
                
                adobe_d1 = adobe_reader_df['Release Date'][0]
                adobe_d2 = adobe_exp_manager_df['Release Date'][0]
                
                adobe_latest_publication = get_adobe_latest_publication(adobe_d1, adobe_d2)
                st.session_state.adobe_latest_publication = adobe_latest_publication # store the latest date in session state
                
                # Product 2
                st.write("Searching for Apache HTTP Server...")
                apache_df = get_apache_updates()
                apache_d1 = apache_df['Update Release Date'][0]
                st.session_state.apache_latest_publication = apache_d1
                
                # Product 3
                st.write("Searching for Apache Tomcat 8")
                apache_tomcat_8_df = get_apache_tomcat_8_updates()
                apache_tomcat_8_d1 = apache_tomcat_8_df["Release Date"][0]
                st.session_state.apache_tomcat_8_latest_publication = apache_tomcat_8_d1
                
                # Product 4
                st.write("Searching for Apache Tomcat 9")
                apache_tomcat_9_df = get_apache_tomcat_9_updates()
                apache_tomcat_9_d1 = apache_tomcat_9_df["Release Date"][0]
                st.session_state.apache_tomcat_9_latest_publication = apache_tomcat_9_d1
                
                # Product 5
                st.write("Searching for Apache Tomcat 10")
                apache_tomcat_10_df = get_apache_tomcat_10_updates()
                apache_tomcat_10_d1 = apache_tomcat_10_df["Release Date"][0]
                st.session_state.apache_tomcat_10_latest_publication = apache_tomcat_10_d1
                
                # Product 6
                st.write("Searching for Apache Tomcat 11")
                apache_tomcat_11_df = get_apache_tomcat_11_updates()
                apache_tomcat_11_d1 = apache_tomcat_11_df["Release Date"][0]
                st.session_state.apache_tomcat_11_latest_publication = apache_tomcat_11_d1
                
                # Product 7
                st.write("Searching for Apple...")
                apple_df = get_apple_updates()
                apple_d1 = apple_df['Release Date'][0]
                st.session_state.apple_latest_publication = apple_d1
                
                # Product 8
                st.write("Searching for Atlassian...")
                atlassian_df = get_atlassian_updates()
                atlassian_d1 = atlassian_df['Title'][0]
                atlassian_d1 = atlassian_d1.replace("Security Bulletin", "").strip()
                st.session_state.atlassian_latest_publication = atlassian_d1
                
                # Product 9
                st.write("Searching for BIND9(ISC)...")
                bind_df = get_bind_updates()
                bind_d1 = bind_df['CVE Number'][0]
                st.session_state.bind_latest_publication = bind_d1
                
                # Product 11
                st.write("Searching for Chrome...")
                chrome_df = get_chrome_updates()
                chrome_d1 = chrome_df['Publish Date'][0]
                st.session_state.chrome_latest_publication = chrome_d1
                
                # Product 12
                st.write("Searching for Cisco...")
                cisco_df = get_cisco_updates()
                cisco_d1 = cisco_df['Last Updated'][0]
                st.session_state.cisco_latest_publication = cisco_d1
                
                # Product 13
                st.write("Searching for Drupal (Core)...")
                drupal_df = get_drupal_updates()
                drupal_d1 = drupal_df['Publication Date'][0]
                st.session_state.drupal_latest_publication = drupal_d1
                
                # Product 15
                st.write("Searching for Fortinet...")
                fortinet_df = get_fortinet_updates()
                fortinet_d1 = fortinet_df['Published On'][0]
                st.session_state.fortinet_latest_publication = fortinet_d1
                
                # Product 16
                st.write("Searching for GitLab...")
                gitlab_df = get_gitlab_updates()
                gitlab_d1 = gitlab_df['Published Date'][0]
                st.session_state.gitlab_latest_publication = gitlab_d1
                
                # Product 17
                st.write("Searching for Intel...")
                intel_df = get_intel_updates()
                intel_d1 = intel_df['Release Date'][0]
                st.session_state.intel_latest_publication = intel_d1
                
                # Product 18
                st.write("Searching for Joomla...")
                joomla_df = get_joomla_updates()
                joomla_d1 = joomla_df['Fixed Date'][0]
                st.session_state.joomla_latest_publication = joomla_d1
                
                # Product 19
                st.write("Searching for Juniper...")
                juniper_df = get_juniper_updates()
                juniper_d1 = juniper_df['Publish Date'][0]
                st.session_state.juniper_latest_publication = juniper_d1
                
                # Product 20
                st.write("Searching for Microsoft...")
                microsoft_df = get_microsoft_updates()
                microsoft_d1 = microsoft_df['Release Date'][0]
                st.session_state.microsoft_latest_publication = microsoft_d1
                
                # Product 21
                st.write("Searching for OpenSSL...")
                openssl_df = get_openssl_updates()
                openssl_d1 = openssl_df['Published at'][0]
                st.session_state.openssl_latest_publication = openssl_d1
                
                # Product 22
                st.write("Searching for Oracle...")
                oracle_df = get_oracle_updates()
                oracle_d1 = oracle_df['Released Date'][0][1:]
                st.session_state.oracle_latest_publication = oracle_d1
                
                # Product 23
                st.write("Searching for Palo Alto...")
                paloalto_df = get_paloalto_updates()
                paloalto_d1 = paloalto_df['Published At'][0]
                st.session_state.paloalto_latest_publication = paloalto_d1
                
                # Product 24
                st.write("Searching for Samba...")
                samba_df = get_samba_updates()
                samba_d1 = samba_df['Date Issued'][0]
                st.session_state.samba_latest_publication = samba_d1
                
                # Product 25
                st.write("Searching for SAP...")
                sap_df = get_sap_updates()
                sap_d1 = sap_df['Date'].iloc[-1]
                st.session_state.sap_latest_publication = sap_d1
                
                # Product 26
                st.write("Searching for SolarWinds...")
                solarwinds_df = get_solarwinds_updates()
                solarwinds_d1 = solarwinds_df['pubDate'][0]
                st.session_state.solarwinds_latest_publication = solarwinds_d1
                
                # Product 27
                st.write("Searching for WordPress...")
                wordpress_df = get_wordpress_updates()
                wordpress_d1 = wordpress_df['Date'][0]
                st.session_state.wordpress_latest_publication = wordpress_d1
                
                status.update(
                    label="Checks complete!", state="complete", expanded=False
                )
            
            # Update the session state to hide the button
            st.session_state.check_status = True
    
    # ====== END: Check for Update Logic ======

    # ====== START: Display Vulnerability Update Table ======
    if st.session_state.check_status:
        # Hide the "Check for updates" button
        button_placeholder.empty()

        st.markdown(
            f"<h4>Latest Vulnerability Updates <span style='font-size:14px;'>(as of {today_date})</span></h4>",
            unsafe_allow_html=True,
        )
        
        # Display the DataFrame and Refresh button
        df = pd.DataFrame(
            [
                {"Product": "1. Adobe Acrobat/Reader & Experience Manager", "Latest Publication": st.session_state.adobe_latest_publication, "Extract": False},
                {"Product": "2. Apache HTTP Server", "Latest Publication": st.session_state.apache_latest_publication, "Extract": False},
                {"Product": "3. Apache Tomcat 8", "Latest Publication": st.session_state.apache_tomcat_8_latest_publication, "Extract": False},
                {"Product": "4. Apache Tomcat 9", "Latest Publication": st.session_state.apache_tomcat_9_latest_publication, "Extract": False},
                {"Product": "5. Apache Tomcat 10", "Latest Publication": st.session_state.apache_tomcat_10_latest_publication, "Extract": False},
                {"Product": "6. Apache Tomcat 11", "Latest Publication": st.session_state.apache_tomcat_11_latest_publication, "Extract": False},
                {"Product": "7. Apple iOS, iPadOS and macOS", "Latest Publication": st.session_state.apple_latest_publication, "Extract": False},
                {"Product": "8. Atlassian Monthly Bulletin", "Latest Publication": st.session_state.atlassian_latest_publication, "Extract": False},
                {"Product": "9. BIND9 (ISC)", "Latest Publication": st.session_state.bind_latest_publication, "Extract": False},
                {"Product": "10. Broadcom VMWare Cloud Foundation (WIP)", "Latest Publication": "N.A (WIP)", "Extract": False},
                {"Product": "11. Chrome Stable Channel Update for Desktop", "Latest Publication": st.session_state.chrome_latest_publication, "Extract": False},
                {"Product": "12. Cisco", "Latest Publication": st.session_state.cisco_latest_publication, "Extract": False},
                {"Product": "13. Drupal Core", "Latest Publication": st.session_state.drupal_latest_publication, "Extract": False},
                {"Product": "14. MyF5", "Latest Publication": "N.A (WIP)", "Extract": False},
                {"Product": "15. Fortinet", "Latest Publication": st.session_state.fortinet_latest_publication, "Extract": False},
                {"Product": "16. GitLab", "Latest Publication": st.session_state.gitlab_latest_publication, "Extract": False},
                {"Product": "17. Intel", "Latest Publication": st.session_state.intel_latest_publication, "Extract": False},
                {"Product": "18. Joomla", "Latest Publication": st.session_state.joomla_latest_publication, "Extract": False},
                {"Product": "19. Juniper", "Latest Publication": st.session_state.juniper_latest_publication, "Extract": False},
                {"Product": "20. Microsoft", "Latest Publication": st.session_state.microsoft_latest_publication, "Extract": False},
                {"Product": "21. OpenSSL", "Latest Publication": st.session_state.openssl_latest_publication, "Extract": False},
                {"Product": "22. Oracle Quarterly Publication", "Latest Publication": st.session_state.oracle_latest_publication, "Extract": False},
                {"Product": "23. Palo Alto", "Latest Publication": st.session_state.paloalto_latest_publication, "Extract": False},
                {"Product": "24. Samba", "Latest Publication": st.session_state.samba_latest_publication, "Extract": False},
                {"Product": "25. SAP", "Latest Publication": st.session_state.sap_latest_publication, "Extract": False},
                {"Product": "26. SolarWinds", "Latest Publication": st.session_state.solarwinds_latest_publication, "Extract": False},
                {"Product": "27. WordPress (Security Releases)", "Latest Publication": st.session_state.wordpress_latest_publication, "Extract": False},
                
            ]
        )
        
        disabled_columns = ("Product", "Latest Publication") # users cannot edit it
        
        # Reference: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.column
        edited_df = st.data_editor(
            df,
            height = 28*35, # 28 row x 35 aprox. height
            use_container_width=True, 
            hide_index=True, 
            disabled=disabled_columns,
            column_config={
            "Product": st.column_config.Column(
                "Product",
                width="large",
            )},
            )

        update_selected_count = len(edited_df[edited_df["Extract"] == True])
        st.markdown(f"You have chosen **<u>{update_selected_count}</u>** product(s) to extract.", unsafe_allow_html=True)
        
    # ====== END: Display Vulnerability Update Table ======
        
    # ====== START: Extract Updates Based on Selected Products ======

        # If there one or more products selected, the scraper will start getting the finer details.
        if update_selected_count > 0:
            if st.button("Start extracting"):
                # Pass the web_scraping function the websites to extract from.
                product_list = list(edited_df[edited_df["Extract"] == True]["Product"])
                web_scraping(product_list)
                
    # ====== END: Extract Updates Based on Selected Products ======
    
        # When user clicks on refresh, hide the dataframe and refresh the interface.
        if st.button("Refresh"):
            st.session_state.check_status = False
            st.rerun() 


def web_scraping(product_list):
    # This function should return dataframe(s) for export
    # Simulating scraping the different websites.
    with st.status("Extracting vulnerability updates ...", expanded=True) as status:
        for product in product_list:
            # If product == this, do this.
            st.write(f"Extracting for {product}...")
            time.sleep(2)
            
        status.update(
            label="Extraction complete!", state="complete", expanded=False
        )
        
        # Set status to True so that Download button can appear
        st.session_state.extraction_status = True
        
    # Once extracted, will display the download button
    if st.session_state.extraction_status:
        
        excel = export_vulnerabilities("df_list should go here")
        
        st.download_button(
        label="Download data as .xlsx",
        data=excel,
        file_name="goi_vulnerability_updates.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    

# Run the function
retrieve_latest_vulnerability_updates()

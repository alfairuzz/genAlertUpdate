import requests
import pandas as pd


def get_microsoft_updates():
    # Search the first 5000 records
    url = "https://api.msrc.microsoft.com/sug/v2.0/en-GB/affectedProduct?$orderBy=releaseDate%20desc&$skip=0&$top=5000"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None, None  # Early return if request fails

    # Collect data into a DataFrame directly using pandas.json_normalize
    export_detail_df = pd.json_normalize(data['value'])

    # Select and rename the columns of interest
    export_detail_df = export_detail_df.rename(columns={
        'releaseDate': 'Release Date',
        'product': 'Product',
        'platform': 'Platform',
        'impact': 'Impact',
        'severity': 'Max Severity',
        'cveNumber': 'CVE'
    })

    # Handle missing values by filling with empty strings
    columns_of_interest = ["Release Date", "Product", "Platform", "Impact", "Max Severity", "CVE"]
    export_detail_df = export_detail_df[columns_of_interest].fillna('')

    # Convert 'Release Date' to datetime
    export_detail_df['Release Date (Raw)'] = pd.to_datetime(
        export_detail_df['Release Date'], format="%Y-%m-%dT%H:%M:%SZ", errors='coerce'
    )

    # Format 'Release Date'
    export_detail_df['Release Date'] = export_detail_df['Release Date (Raw)'].dt.strftime("%b %d, %Y")

    # Sort by 'Release Date (Raw)' descending
    export_detail_df = export_detail_df.sort_values(by='Release Date (Raw)', ascending=False)

    # Get the 5 most recent 'Release Date's
    result_filter = export_detail_df['Release Date'].unique()[:5]

    # Filter the DataFrame
    filtered_df = export_detail_df[export_detail_df['Release Date'].isin(result_filter)]

    # Group by 'Release Date' and count unique 'CVE's
    summary_df = filtered_df.groupby('Release Date').agg({'CVE': pd.Series.nunique}).reset_index()
    summary_df.columns = ['Release Date', 'Unique CVE(s)']

    # Add 'Category' column
    summary_df['Category'] = summary_df['Unique CVE(s)'].apply(
        lambda x: "Microsoft Security Release" if x > 50 else "Out-of-Band Microsoft Security Release"
    )

    # Rearrange columns
    summary_df = summary_df[['Release Date', 'Category', 'Unique CVE(s)']]
    summary_df['Release Date (sort)'] = pd.to_datetime(summary_df['Release Date'], format="%b %d, %Y")
    summary_df.sort_values(by="Release Date (sort)", ascending=False, inplace=True)
    summary_df = summary_df[['Release Date', 'Category', 'Unique CVE(s)']]
    
    
    summary_df = summary_df.reset_index(drop=True)

    return summary_df

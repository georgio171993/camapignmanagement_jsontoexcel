
import json
import pandas as pd
import openpyxl
from datetime import datetime
import streamlit as st

# Function to process the JSON file and convert it to Excel
def process_json(json_file):
    # Load the JSON data from the uploaded file
    data = json.load(json_file)

    # Prepare the data for Excel
    rows = []
    for record in data:
        if record['userType'] == 'grandparent':
            grandparent_name = record['name']
            grandparent_email = record['email']
            grandparent_status = record['status']
            sourcing_domain = record['additionalData'].get('sourcingDomain', '')
            loreal_ksm_lpo = record['additionalData'].get('lorealKsmLpo', '')
            sourcing_Id = record['additionalData'].get('sourcingId', '')
            
            # If there are children (invoicing sites)
            if 'childList' in record:
                for child in record['childList']:
                    if child['userType'] == 'child':
                        invoicing_site_name = child['name']
                        invoicing_site_email = child['email'] if child['email'] else grandparent_email
                        invoicing_site_status = child['status']
                        
                        # Append to rows
                        rows.append([grandparent_name, grandparent_email, grandparent_status, sourcing_domain, loreal_ksm_lpo, sourcing_Id,
                                    invoicing_site_name, invoicing_site_email, invoicing_site_status])
                        
            else:  # No child records, just grandparent
                rows.append([grandparent_name, grandparent_email, grandparent_status, sourcing_domain, loreal_ksm_lpo, sourcing_Id,
                            '', '', ''])
                
            # Ensure the grandparent fields are only filled once
            grandparent_name = grandparent_email = grandparent_status = sourcing_domain = loreal_ksm_lpo = sourcing_Id = ''
            
    # Create a DataFrame from the rows
    columns = [
        "Grandparent Company (1.2.1)", 
        "Grandparent Email (1.1.9)", 
        "Grandparent Status", 
        "L'Oréal KSM Sourcing Domain (1.1.2)",
        "L'Oréal KSM LPO (Zones) (1.1.6.)", 
        "Parent Company ID MySourcing (1.2.3)",
        "Invoicing Site For GP (1.4.1)", 
        "Invoicing Site Email (1.4.10)", 
        "Invoicing Site Status"
    ]

    df = pd.DataFrame(rows, columns=columns)

    # Get today's date in the format DD MMM YYYY (e.g., 07 Oct 2024)
    today_date = datetime.now().strftime('%d %b %Y')

    # Format the output file name with today's date
    output_file = f"L'Oreal Campaign Status - {today_date}.xlsx"

    # Write the DataFrame to the Excel file
    df.to_excel(output_file, index=False)

    return output_file

# Streamlit app
st.title("JSON to Excel Converter")

# File uploader to accept JSON file
uploaded_file = st.file_uploader("Upload your JSON file", type=["json"])

if uploaded_file is not None:
    # Process the uploaded JSON file and convert it to Excel
    st.write("Processing your file...")
    output_file = process_json(uploaded_file)

    # Provide download button for the generated Excel file
    with open(output_file, "rb") as f:
        st.download_button("Download the Excel file", f, file_name=output_file)

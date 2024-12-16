import streamlit as st
import os

st.title("Download Data")
st.subheader("Select the data you want to download")

# assign directory
directory = 'data'
 
for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith('.csv'):  # Ensure it's a CSV file
            file_path = os.path.join(root, filename)
            # Read file content
            with open(file_path, 'r') as file:
                file_content = file.read()
            
            # Create download button
            st.download_button(
                label=filename.replace('.csv', ''),
                data=file_content,
                file_name=filename,
                mime='text/csv'
            )
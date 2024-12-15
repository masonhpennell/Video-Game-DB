import streamlit as st
import os

st.title("Download Data")
st.subheader("Select the data you want to download")

# assign directory
directory = 'data'
 
# iterate over files in
# that directory
for root, dirs, files in os.walk(directory):
    for filename in files:
        print(os.path.join(root, filename))
        st.download_button(label=filename.replace('.csv',''),
            data=os.path.join(root, filename), file_name=filename)
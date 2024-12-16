import streamlit as st
import os

st.title("Download Data")

# Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Search for a game")

st.subheader("Select the data you want to download")

# assign directory
directory = 'data'
 
# iterate over files in
# that directory
for root, dirs, files in os.walk(directory):
    for filename in files:
        st.download_button(label=filename.replace('.csv',''),
            data=os.path.join(root, filename), file_name=filename)
        

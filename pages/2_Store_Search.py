import streamlit as st
import pandas as pd

cursor = st.session_state['cursor']

st.title("Search for a store")

location = st.text_input("Store Location")

cursor.execute(f"SELECT * FROM store WHERE location LIKE '{location}%';")
data = cursor.fetchall()
df = pd.DataFrame(data, columns=cursor.column_names)
st.table(df)
import mysql.connector
import streamlit as st

conn = st.session_state['conn']
cursor = st.session_state['cursor']
st.write(conn)
import streamlit as st
import pandas as pd

conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Create a user")

name = st.text_input("Enter Name: ")
password = st.text_input("Enter Password: ")  # Ask for the password

# Check if the UserID already exists
cursor.execute(f"SELECT MAX(userID) FROM user;")
user_id = cursor.fetchone()[0]

# If UserID is unique, proceed with inserting the new user
if st.button("Create User"):
    cursor.execute(f"INSERT INTO user (name, password) VALUES ('{name}', '{password}');")
    conn.commit()
    st.write(f"User {name} with UserID {user_id + 1} created successfully.")
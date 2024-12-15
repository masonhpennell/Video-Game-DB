import streamlit as st
import pandas as pd

conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Create a user")

user_id = st.number_input("Enter UserID: ", 0, 100000, 0, 1)
name = st.text_input("Enter Name: ")
password = st.text_input("Enter Password: ")  # Ask for the password

# Check if the UserID already exists
cursor.execute(f"SELECT COUNT(*) FROM user WHERE userID = {user_id};")
result = cursor.fetchone()[0]

if result > 0:
    st.write("Error: The UserID is already in use. Please enter a new UserID.")
# If UserID is unique, proceed with inserting the new user
if st.button("Create User"):
    cursor.execute(f"INSERT INTO user (userID, name, password) VALUES ({user_id}, '{name}', '{password}');")
    conn.commit()
    st.write(f"User {name} with UserID {user_id} created successfully.")
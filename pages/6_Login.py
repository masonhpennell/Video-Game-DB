import streamlit as st
import mysql.connector
import bcrypt

# Database connection
conn = st.session_state['conn']
cursor = st.session_state['cursor']

# Ensure session state values
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("User Login")

# Tab structure for Login and Registration
tab1, tab2 = st.tabs(["Login", "Create New User"])

# --- LOGIN TAB ---
with tab1:
    if not st.session_state.logged_in:
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Login"):
            # Query database for the user
            cursor.execute("SELECT password FROM user WHERE name = %s", (username,))
            result = cursor.fetchone()
            
            if result:
                stored_hashed_password = result[0]
                if bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password.encode("utf-8")):
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()

                else:
                    st.error("Incorrect password. Try again.")
            else:
                st.error("Username not found.")
    else:
        st.success(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()


# --- CREATE NEW USER TAB ---
with tab2:
    st.subheader("Create a New User")
    new_username = st.text_input("New Username", placeholder="Enter your username")
    new_password = st.text_input("New Password", type="password", placeholder="Enter your password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

    if st.button("Create Account"):
        if new_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        elif not new_username or not new_password:
            st.error("Username and password cannot be empty.")
        else:
            # Check if username already exists
            cursor.execute("SELECT COUNT(*) FROM user WHERE name = %s", (new_username,))
            if cursor.fetchone()[0] > 0:
                st.error("Username already exists. Please choose a different one.")
            else:
                # Hash the password and insert into the database
                hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                cursor.execute("INSERT INTO user (name, password) VALUES (%s, %s)", (new_username, hashed_password))
                conn.commit()
                st.success("Account created successfully! Please log in.")


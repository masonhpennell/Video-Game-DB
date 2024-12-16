import streamlit as st
import pandas as pd

conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Delete a game")

# Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Search for a game")

cursor.execute('SELECT COUNT(*) FROM game;')
max = cursor.fetchone()[0]
id = st.number_input("Enter game ID", 0, max, 0, 1)
if (st.button("Delete this game?")):
    cursor.execute("START TRANSACTION;")
    cursor.execute(f"UPDATE game SET isDeleted = 1 WHERE gameID = {id};")
    cursor.execute("COMMIT;")
    conn.commit()

deleted = st.checkbox("Show deleted games")
cursor.execute(f'SELECT gameID, title FROM game WHERE isDeleted = {deleted};')
data = cursor.fetchall()
df = pd.DataFrame(data, columns=cursor.column_names)
st.table(df)


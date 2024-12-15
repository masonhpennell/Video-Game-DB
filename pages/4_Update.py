import streamlit as st
import pandas as pd

conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Update a game")

cursor.execute('SELECT COUNT(*) FROM game;')
max = cursor.fetchone()[0]
id = st.number_input("Enter game ID", 0, max, 0, 1)
# todo
@st.dialog("Enter a new value:")
def update(attribute):
    value = st.text_input("new value", label_visibility="collapsed")
    if st.button("Submit"):
        cursor.execute(f"UPDATE Game SET {attribute} = '{value}' WHERE GameID = {id};")
        conn.commit()

col1, col2, col3 = st.columns(3)
st.write("Which value would you like to update?")
with col1:
    if st.button("title", use_container_width=True):
        update("title")
with col2:
    if st.button("genre", use_container_width=True):
        update("genre")
with col3:
    if st.button("rating", use_container_width=True):
        update("rating")

cursor.execute(f'SELECT gameID, title, genre, rating FROM game WHERE isDeleted = 0 AND gameID = {id};')
data = cursor.fetchall()
df = pd.DataFrame(data, columns=cursor.column_names)
st.table(df)
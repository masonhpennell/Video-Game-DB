import streamlit as st
import pandas as pd

conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Delete a game")

#Aggregate function
cursor.execute('SELECT COUNT(*) FROM game;')
max = cursor.fetchone()[0]
id = st.number_input("Enter game ID", 0, max, 0, 1)
if (st.button("Delete this game?")):
    #Make ue of transactions
    cursor.execute("START TRANSACTION;")
    cursor.execute(f"UPDATE game SET isDeleted = 1 WHERE gameID = {id};")
    cursor.execute("COMMIT;")
    conn.commit()

deleted = st.checkbox("Show deleted games")
cursor.execute(f'SELECT gameID, title FROM game WHERE isDeleted = {deleted};')
data = cursor.fetchall()
df = pd.DataFrame(data, columns=cursor.column_names)
st.table(df)
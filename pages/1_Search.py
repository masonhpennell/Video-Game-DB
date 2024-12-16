import streamlit as st
import pandas as pd

conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Search for a game")

title = st.text_input("Game Title")

# Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Search for a game")

cursor.execute("SELECT name FROM developer;")
developers = [d for (d,) in cursor.fetchall()]
cursor.execute("SELECT name FROM publisher;")
publishers = [p for (p,) in cursor.fetchall()]
developer = st.radio("Developer", developers, horizontal=True)
publisher = st.radio("Publisher", publishers, horizontal=True)
min = st.slider("Minimum Rating", 0.0, 10.0, 0.0, 0.1)

cursor.execute(f'''
               SELECT title, rating
               FROM game
               WHERE title LIKE '{title}%' AND developerID in (
                   SELECT developerID
                   FROM developer
                   WHERE name = '{developer}'
               ) AND publisherID in (
                   SELECT publisherID
                   FROM publisher
                   WHERE name = '{publisher}'
               ) AND rating >= {min};
               ''')
data = cursor.fetchall()
df = pd.DataFrame(data, columns=cursor.column_names)
st.table(df)




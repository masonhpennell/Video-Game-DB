import streamlit as st
import pandas as pd

cursor = st.session_state['cursor']

st.title("Search for a game")

title = st.text_input("Game Title")

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
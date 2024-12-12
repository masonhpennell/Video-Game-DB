import streamlit as st

title = st.text_input(
    "Enter a name"
)

# Perform query.
df = st.session_state.key.query(F'''
    SELECT title
    FROM film
    WHERE title LIKE '{title}%';
''')

# Print results.
for row in df.itertuples():
    st.write(f"{row.title}")
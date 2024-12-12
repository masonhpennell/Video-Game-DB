import mysql.connector
import streamlit as st
import pandas as pd

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    # conn = mysql.connector.connect(
    #             host = 'localhost',
    #             user = 'root',
    #             password = 'mason918'
    #         )
    # cursor = conn.cursor()

    # cursor.execute("CREATE SCHEMA IF NOT EXISTS VideoGames;")

st.session_state['conn'] = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'mason918',
            database = 'sakila'
        )
st.session_state['cursor'] = st.session_state['conn'].cursor()
conn = st.session_state['conn']
cursor = st.session_state['cursor']

st.title("Search for a movie")

title = st.text_input("Movie title")

developer = st.radio("Developer", ['Nintendo', 'Sega', 'Sony', 'Microsoft'], horizontal=True)
publisher = st.radio("Publisher", ['Nintendo', 'Sega', 'Sony', 'Microsoft'], horizontal=True)

cursor.execute(f"SELECT title FROM film WHERE title LIKE '{title}%';")
data = cursor.fetchall()
df = pd.DataFrame(data, columns=cursor.column_names)
st.dataframe(df)

    
# # Connect to MySQL server (make sure MySQL server is running)
# db_connection = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='mason918'
# )

# db_cursor = db_connection.cursor()

# # Create a database
# db_cursor.execute("CREATE DATABASE IF NOT EXISTS VideoGames")

# # Select the database
# db_cursor.execute("USE VideoGames")

# # Create a table
# db_cursor.execute("""
# CREATE TABLE IF NOT EXISTS games (
#     gameID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
#     Title VARCHAR(50) NOT NULL,
#     Genre VARCHAR(50) NOT NULL
# );
# """)

# # Insert data
# db_cursor.execute("INSERT INTO games (title, genre) VALUES ('Mario', 'Platformer')")
# db_cursor.execute("INSERT INTO games (title, genre) VALUES ('Zelda', 'Adventure')")
# db_cursor.execute("INSERT INTO games (title, genre) VALUES ('Pokemon', 'RPG')")

# # Commit the changes
# db_connection.commit()

# # Retrieve data
# db_cursor.execute("SELECT * FROM games")
# result = db_cursor.fetchall()

# # Close the connection
# db_cursor.close()
# db_connection.close()

# # Display data using Streamlit
# st.title('User Data')
# for row in result:
#     st.write(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

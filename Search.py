import mysql.connector
import streamlit as st
import pandas as pd

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'mason918'
            )
    cursor = conn.cursor()

    cursor.execute("CREATE SCHEMA IF NOT EXISTS VideoGames;")

    conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'mason918',
                database = 'VideoGames'
            )
    cursor = conn.cursor()
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS game(
                gameID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                rating FLOAT(3, 2) NOT NULL,
                genre VARCHAR(50),
                title VARCHAR(50) NOT NULL,
                developerID INT NOT NULL,
                storeID INT NOT NULL,
                publisherID INT NOT NULL
            );
        ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS developer(
                developerID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS publisher(
                publisherID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        ''')
    
    cursor.execute('''
            INSERT INTO developer (name) VALUES
                ('Naughty Dog'),
                ('Rockstar Games'),
                ('Blizzard Entertainment'),
                ('CD Projekt Red'),
                ('Bethesda Game Studios');
            ''')
    
    cursor.execute('''
            INSERT INTO publisher (name) VALUES
                ('Sony Interactive Entertainment'),
                ('Take-Two Interactive'),
                ('Activision Blizzard'),
                ('CD Projekt'),
                ('Bethesda Softworks');
            ''')
    
    cursor.execute('''
            INSERT INTO game (rating, genre, title, developerID, storeID, publisherID) VALUES
                (9.5, 'Action-Adventure', 'The Last of Us Part II', 1, 1, 1),
                (9.7, 'Open World', 'Red Dead Redemption 2', 2, 2, 2),
                (9.3, 'RPG', 'The Witcher 3: Wild Hunt', 4, 3, 4),
                (9.0, 'FPS', 'DOOM Eternal', 5, 4, 5),
                (8.8, 'MOBA', 'Overwatch', 3, 5, 3);
            ''')
    
    conn.commit()
    
st.session_state['conn'] = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'mason918',
            database = 'VideoGames'
        )
st.session_state['cursor'] = st.session_state['conn'].cursor()
conn = st.session_state['conn']
cursor = st.session_state['cursor']
st.title("Search for a game")

title = st.text_input("Game Title")

cursor.execute("SELECT name FROM developer;")
developers = [d for (d,) in cursor.fetchall()]
cursor.execute("SELECT name FROM publisher;")
publishers = [p for (p,) in cursor.fetchall()]
developer = st.radio("Developer", developers, horizontal=True)
publisher = st.radio("Publisher", publishers, horizontal=True)

cursor.execute(f'''
               SELECT title
               FROM game
               WHERE title LIKE '{title}%' AND developerID in (
                   SELECT developerID
                   FROM developer
                   WHERE name = '{developer}'
               ) AND publisherID in (
                   SELECT publisherID
                   FROM publisher
                   WHERE name = '{publisher}'
              );
               ''')
data = cursor.fetchall()
df = pd.DataFrame(data, columns=cursor.column_names)
st.dataframe(df)

# db_cursor.close()
# db_connection.close()

# # Display data using Streamlit
# st.title('User Data')
# for row in result:
#     st.write(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

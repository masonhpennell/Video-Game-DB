import mysql.connector
import streamlit as st
from helper import helper

def create_tables():
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
                publisherID INT NOT NULL,
                isDeleted BOOLEAN DEFAULT FALSE
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
            CREATE TABLE IF NOT EXISTS user(
                userID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS store(
                storeID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                gameID INT NOT NULL
            );
        ''')
    
    populate_tables('game', cursor)
    populate_tables('developer', cursor)
    populate_tables('publisher', cursor)
    conn.commit()
    
def is_empty(table, cursor):
    #query to get count of songs in table
    query = f'''
    SELECT COUNT(*)
    FROM {table};
    '''
    #run query and return value
    cursor.execute(query)
    return cursor.fetchone()[0] == 0

def populate_tables(name, cursor):
    if is_empty(name, cursor):
        data = helper.data_cleaner(f"data/{name}.csv")
        attribute_count = len(data[0])
        placeholders = (f"%s,"*attribute_count)[:-1]
        query = f"INSERT INTO {name} VALUES("+placeholders+")"
        cursor.executemany(query, data)
        
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    create_tables()
st.session_state['conn'] = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'mason918',
            database = 'VideoGames'
        )
st.session_state['cursor'] = st.session_state['conn'].cursor()

st.title("Welcome to our Video Game Database!")
st.subheader("Click the links on the right to navigate the site.")
st.image("image.jpg", use_container_width=True)
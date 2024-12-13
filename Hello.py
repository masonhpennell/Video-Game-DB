import mysql.connector
import streamlit as st
import pandas as pd
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
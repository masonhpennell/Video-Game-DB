import mysql.connector
import sqlite3
from helper import helper


class db_operations():
    def __init__(self, db_name):
        
        # creating the connection to the database
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'CPSC_408',
            auth_plugin = 'mysql_native_password',
            database = db_name
        )

        # create cursor object to interact with database
        self.cur_obj = self.conn.cursor()
        print(f"connected to the VideoGameProject database successfully")

    def modify_query(self, query):
        self.cur_obj.execute(query)
        self.conn.commit()

    def create_table(self):

        create_users = '''
        CREATE TABLE IF NOT EXISTS User(
            UserID INT NOT NULL PRIMARY KEY,
            Name VARCHAR(255) NOT NULL,
            Password VARCHAR(255) NOT NULL
            );
        '''

        create_publisher = '''
            CREATE TABLE IF NOT EXISTS Publisher(
                PublisherID INT NOT NULL PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                Location VARCHAR(255) NOT NULL
            );
        '''

        create_developer = '''
            CREATE TABLE IF NOT EXISTS Developer(
                DeveloperID INT NOT NULL PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                Location VARCHAR(255) NOT NULL
            );
        '''

        create_store = '''
            CREATE TABLE IF NOT EXISTS Store(
                StoreID INT NOT NULL PRIMARY KEY,
                Location VARCHAR(255) NOT NULL
            );
        '''

        create_game = '''
            CREATE TABLE IF NOT EXISTS Game(
                GameID INT NOT NULL PRIMARY KEY,
                Rating INT NOT NULL,
                Genre VARCHAR(255) NOT NULL,
                Title VARCHAR(255) NOT NULL,
                DeveloperID INT NOT NULL,
                StoreID INT NOT NULL,
                PublisherID INT NOT NULL,
                IsDeleted BOOLEAN DEFAULT FALSE, 
                FOREIGN KEY (DeveloperID) REFERENCES Developer(DeveloperID),
                FOREIGN KEY (StoreID) REFERENCES Store(StoreID),
                FOREIGN KEY (PublisherID) REFERENCES Publisher(PublisherID)
            );
        '''

        # Connect to the database to create tables in VideoGameProject database
        self.cur_obj.execute(create_users)
        self.cur_obj.execute(create_publisher)
        self.cur_obj.execute(create_developer)
        self.cur_obj.execute(create_store)
        self.cur_obj.execute(create_game)

        print("tables created")

    #load some pre-existing data froma CSV file for all the following tables
    def populate_user_table(self, filepath):
        data = helper.data_cleaner(filepath)
        print("Data to insert into User table:", data)  
        query = '''
            INSERT INTO User (UserID, Name, Password)
            VALUES (%s, %s, %s)
        '''
        self.bulk_insert(query, data)  # Use the bulk_insert method
        print("User table populated successfully.")

    def populate_game_table(self, filepath):
        data = helper.data_cleaner(filepath)
        query = '''
            INSERT INTO Game (GameID, Rating, Genre, Title, DeveloperID, StoreID, PublisherID, IsDeleted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.bulk_insert(query, data)
        print("Game table populated successfully.")

    def populate_publisher_table(self, filepath):
        data = helper.data_cleaner(filepath)
        query = '''
            INSERT INTO Publisher (PublisherID, Name, Location)
            VALUES (%s, %s, %s)
        '''
        self.bulk_insert(query, data)
        print("Publisher table populated successfully.")

    def populate_developer_table(self, filepath):
        data = helper.data_cleaner(filepath)
        query = '''
            INSERT INTO Developer (DeveloperID, Name, Location)
            VALUES (%s, %s, %s)
        '''
        self.bulk_insert(query, data)
        print("Developer table populated successfully.")

    def populate_store_table(self, filepath):
        data = helper.data_cleaner(filepath)
        query = '''
            INSERT INTO Store (StoreID, Location)
            VALUES (%s, %s)
        '''
        self.bulk_insert(query, data)
        print("Store table populated successfully.")

    # function for bulk inserting records
    # best used for inserting many records with parameters
    def bulk_insert(self, query, data):
        self.cur_obj.executemany(query, data)
        self.conn.commit()

    #function for soft deletion, changes the IsDeleted value of a game to 1(True)
    def soft_delete_game(self, game_id):
        query = '''
            UPDATE Game
            SET IsDeleted = 1
            WHERE GameID = %s;
        '''
        self.cur_obj.execute(query, (game_id,))
        self.conn.commit()
        print(f"Game with GameID {game_id} marked as deleted.")

    #function to get all games regardless of whether they were deleted or not
    def get_all_games(self):
        query = '''
            SELECT GameID, Title, IsDeleted
            FROM Game;
        '''
        self.cur_obj.execute(query)
        return self.cur_obj.fetchall()
    
    #function to get only non-delted games
    def get_non_deleted_games(self):
        query = '''
            SELECT GameID, Title
            FROM Game
            WHERE IsDeleted = 0;
        '''
        self.cur_obj.execute(query)
        return self.cur_obj.fetchall()
    
    #function to get only deleted games
    def get_deleted_games(self):
        query = '''
            SELECT GameID, Title
            FROM Game
            WHERE IsDeleted = 1;
        '''
        self.cur_obj.execute(query)
        return self.cur_obj.fetchall()
    


    # function to download info to csv
    # might have to change params 
    def download_to_csv(self):
        pass

    def dowload_to_excel(self):
        pass


    


    # function to close connection to database 
    def close_conn(self):
        # close connection to database
        self.cur_obj.close()
        print('database connection closed.')





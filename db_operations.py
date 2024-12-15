import mysql.connector
import sqlite3
from helper import helper


class db_operations():
    def __init__(self, db_name):
        
        # creating the connection to the database
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'CPSC408!',
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
    

    # Function to create a dynamic User View
    def create_user_view(self, field, value):
        view_query = f'''
            CREATE OR REPLACE VIEW UserView AS
            SELECT UserID, Name
            FROM User
            WHERE {field} = %s;
        '''
        self.cur_obj.execute(view_query, (value,))
        self.conn.commit()
        # print("Dynamic UserView created successfully.")

    def create_game_view(self, field, value, operator="="):
        # Handle mapping of ID fields to human-readable names
        field_mappings = {
            "DeveloperID": "Developer.Name",
            "PublisherID": "Publisher.Name",
            "StoreID": "Store.Location"
        }

        field_to_select = field_mappings.get(field, field)

        # Dynamically build the view query
        view_query = f'''
            CREATE OR REPLACE VIEW GameView AS
            SELECT 
                g.Title, 
                g.Genre, 
                g.Rating, 
                d.Name AS Developer, 
                p.Name AS Publisher, 
                s.Location AS Store
            FROM 
                Game g
            JOIN 
                Developer d ON g.DeveloperID = d.DeveloperID
            JOIN 
                Publisher p ON g.PublisherID = p.PublisherID
            JOIN 
                Store s ON g.StoreID = s.StoreID
            WHERE 
                g.IsDeleted = 0;
        '''

        self.cur_obj.execute(view_query, (value,))
        self.conn.commit()
        print("GameView created successfully.")

    def query_store_by_location(self, location):
        # Query to check if any store exists with the given location
        query = "SELECT StoreID, Location FROM Store WHERE Location LIKE %s;"
        self.cur_obj.execute(query, (f"%{location}%",))
        stores = self.cur_obj.fetchall()

        if stores:
            # If found, create a view that excludes the StoreID, only displaying Location
            view_query = '''
                CREATE OR REPLACE VIEW StoreView AS
                SELECT Location
                FROM Store
                WHERE Location LIKE %s;
            '''
            self.cur_obj.execute(view_query, (f"%{location}%",))
            self.conn.commit()
            print(f"\nStore(s) found with location matching '{location}':")
            print(f"{'Location':<30}")
            for store in stores:
                print(f"{store[1]:<30}")
        else:
            print(f"\nNo stores found with location matching '{location}'.")

    def query_developer_by_name(self, name):
        # Query to find a developer by name
        query = "SELECT DeveloperID, Name, Location FROM Developer WHERE Name LIKE %s;"
        self.cur_obj.execute(query, (f"%{name}%",))
        developers = self.cur_obj.fetchall()

        if developers:
            print(f"\nDeveloper(s) found with name matching '{name}':")
            for dev in developers:
                print(f"Name: {dev[1]}, Location: {dev[2]}")
        else:
            print(f"\nNo developers found with the name '{name}'.")

    def query_developer_by_location(self, location):
        # Query to find a developer by location
        query = "SELECT DeveloperID, Name, Location FROM Developer WHERE Location LIKE %s;"
        self.cur_obj.execute(query, (f"%{location}%",))
        developers = self.cur_obj.fetchall()

        if developers:
            print(f"\nDeveloper(s) found with location matching '{location}':")
            for dev in developers:
                print(f"Name: {dev[1]}, Location: {dev[2]}")
        else:
            print(f"\nNo developers found with the location '{location}'.")

    def query_publisher_by_name(self, name):
        # Query to find a publisher by name
        query = "SELECT PublisherID, Name, Location FROM Publisher WHERE Name LIKE %s;"
        self.cur_obj.execute(query, (f"%{name}%",))
        publishers = self.cur_obj.fetchall()

        if publishers:
            print(f"\nPublisher(s) found with name matching '{name}':")
            for pub in publishers:
                print(f"Name: {pub[1]}, Location: {pub[2]}")
        else:
            print(f"\nNo publishers found with the name '{name}'.")

    def query_publisher_by_location(self, location):
        # Query to find a publisher by location
        query = "SELECT PublisherID, Name, Location FROM Publisher WHERE Location LIKE %s;"
        self.cur_obj.execute(query, (f"%{location}%",))
        publishers = self.cur_obj.fetchall()

        if publishers:
            print(f"\nPublisher(s) found with location matching '{location}':")
            for pub in publishers:
                print(f"Name: {pub[1]}, Location: {pub[2]}")
        else:
            print(f"\nNo publishers found with the location '{location}'.")


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

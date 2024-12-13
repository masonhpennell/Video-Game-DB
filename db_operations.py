import mysql.connector


class db_operations():
    def __init__(self, db_name):
        
        # creating the connection to the database
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'Pps623432',
            auth_plugin = 'mysql_native_password',
            database = db_name
        )

        # create cursor object to interact with database
        self.cur_obj = self.conn.cursor()
        print(f"connected to the VideoGameProject database successfully")



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






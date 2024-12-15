#imports
import os
from helper import helper
from db_operations import db_operations


'''
THIS FILE IS FOR YOU TO CREATE THE FRONTEND 

'''


# initialize db_operations with VideoGameProject database
db_ops = db_operations("VideoGameProject")

def navigation():
    # create the navigation bar
    pass



'''
call functions from db_operations to download info to csv or excel file
    - syntax to call function: 
        db_ops.download_to_csv()

create button(s) to download the info you want

'''



def start_app():
    print("\nWelcome to the ultimate video game database!")

    #create database and tables, run only once. Populate 1 at a time.
    #db_ops.create_table()
    #db_ops.populate_user_table("users.csv")
    #db_ops.populate_publisher_table("publishers.csv")
    #db_ops.populate_developer_table("developers.csv")
    #db_ops.populate_store_table("stores.csv")
    #db_ops.populate_game_table("games.csv")

    
    while True:
        user_choice = main_menu()
        if user_choice == 1:
            view_records_menu()
        if user_choice == 2:
            create_new_record_menu()
        if user_choice == 3:
           soft_delete_record_menu()
        if user_choice == 4:
            update_record_menu()
        if user_choice == 5:
            print("Thank you for using our app! Goodbye!")
            break


def main_menu():
    #for testing purposes, replace with buttons/navigation here
    print(''' \nSelect from the following menu items.
          1. View records menu
          2. Create record menu
          3. Delete record menu
          4. Update record menu
          5. Exit
    ''')
    return helper.get_choice([1,2,3,4,5])


def view_records_menu():
    while True:
        print("\nView Records Menu")
        print("1. Display all records in the database")
        print("2. Display all records of a certain table")
        print("3. Find specific records")
        print("4. Back to Main Menu")

        choice = helper.get_choice([1, 2, 3, 4])

        if choice == 1:
            display_all_records()
        elif choice == 2:
            display_table_records()
        elif choice == 3:
            query_specific_records()
        elif choice == 4:
            break

def display_all_records():
    print("\nDisplaying all records in the database:")
    # Display all records from each table
    tables = ["User", "Publisher", "Developer", "Store", "Game"]
    for table in tables:
        print(f"\n--- {table} Records ---")
        query = f"SELECT * FROM {table};"
        db_ops.cur_obj.execute(query)
        rows = db_ops.cur_obj.fetchall()
        for row in rows:
            print(row)

def display_table_records():
    print("\nChoose a table to display records:")
    print("1. User")
    print("2. Publisher")
    print("3. Developer")
    print("4. Store")
    print("5. Game")
    print("6. Back to View Records Menu")

    choice = helper.get_choice([1, 2, 3, 4, 5, 6])
    tables = ["User", "Publisher", "Developer", "Store", "Game"]

    if choice == 6:
        return

    table_name = tables[choice - 1]
    print(f"\nDisplaying records from {table_name} table:")
    query = f"SELECT * FROM {table_name};"
    db_ops.cur_obj.execute(query)
    rows = db_ops.cur_obj.fetchall()
    for row in rows:
        print(row)

def query_specific_records():
    print("\nFind Specific Records")
    print("1. Developer")
    print("2. Publisher")
    print("3. Game")
    print("4. Store")
    print("5. User")
    print("6. Back to View Records Menu")

    choice = helper.get_choice([1, 2, 3, 4, 5, 6])

    if choice == 6:
        return

    if choice == 5:  # Query for a specific user

        print("\nQuery User Records")
        print("1. Search by Name")
        print("2. Search by ID")
        print("3. Back to Find Specific Records Menu")

        user_choice = helper.get_choice([1, 2, 3])

        if user_choice == 3:
            return

        if user_choice == 1:  # Search by Name
            name = input("Enter the name of the user: ").strip()
            db_ops.create_user_view('Name', name)
        elif user_choice == 2:  # Search by ID
            user_id = input("Enter the UserID of the user: ").strip()
            db_ops.create_user_view('UserID', user_id)

        query = "SELECT UserID, Name FROM UserView;"
        db_ops.cur_obj.execute(query)

        user_record = db_ops.cur_obj.fetchone()
        
        if user_record:
            print("\nUser Found:")
            print(f"UserID: {user_record[0]}")
            print(f"Name: {user_record[1]}")
        else:
            print("\nNo user found with the given information.")

    if choice == 4:  # Query for a specific store
        print("\nFind Specific Store Records")
        print("1. Search by Location")
        print("2. Back to Find Specific Records Menu")
        
        user_choice = helper.get_choice([1, 2])

        if user_choice == 2:
            return

        if user_choice == 1:  # Search by Location
            location = input("Enter the location of the store: ").strip()
            db_ops.query_store_by_location(location)

    if choice == 3:  # Query for a specific game
        print("\nFind Specific Records for Games")
        print("1. Search by Title")
        print("2. Search by Genre")
        print("3. Search by Rating")
        print("4. Search by Developer ID")
        print("5. Search by Publisher ID")
        print("6. Search by Store ID")
        print("7. Back to View Records Menu")

        choice = helper.get_choice([1, 2, 3, 4, 5, 6, 7])

       # Initialize the query to be reused in every case
        query = """
            CREATE OR REPLACE VIEW GameView AS
            SELECT g.Title, g.Genre, g.Rating, d.Name AS Developer, p.Name AS Publisher, s.Location AS Store
            FROM Game g
            JOIN Developer d ON g.DeveloperID = d.DeveloperID
            JOIN Publisher p ON g.PublisherID = p.PublisherID
            JOIN Store s ON g.StoreID = s.StoreID
            WHERE g.IsDeleted = 0
        """
    
        # Handle Title search
        if choice == 1:
            title = input("Enter the title or part of the title: ").strip()
            query += f" AND g.Title LIKE %s"
            params = (f"%{title}%",)

        # Handle Genre search
        elif choice == 2:
            genre = input("Enter the genre: ").strip()
            query += f" AND g.Genre LIKE %s"
            params = (f"%{genre}%",)

        # Handle Rating search
        elif choice == 3:
            print("Would you like to search for games with a rating:")
            print("1. Above a certain threshold")
            print("2. Below a certain threshold")
            threshold_choice = helper.get_choice([1, 2])

            threshold = int(input("Enter the rating threshold (0 to 100): ").strip())
            if threshold_choice == 1:
                query += f" AND g.Rating >= %s"
                params = (threshold,)
            else:
                query += f" AND g.Rating <= %s"
                params = (threshold,)

        # Handle Developer ID search
        elif choice == 4:
            dev_id = int(input("Enter the Developer ID: ").strip())
            query += f" AND g.DeveloperID = %s"
            params = (dev_id,)

        # Handle Publisher ID search
        elif choice == 5:
            pub_id = int(input("Enter the Publisher ID: ").strip())
            query += f" AND g.PublisherID = %s"
            params = (pub_id,)

        # Handle Store ID search
        elif choice == 6:
            store_id = int(input("Enter the Store ID: ").strip())
            query += f" AND g.StoreID = %s"
            params = (store_id,)

        # Execute the query to create or replace the view
        db_ops.cur_obj.execute(query, params)
        db_ops.conn.commit()

        # Fetch and display results
        db_ops.cur_obj.execute("SELECT Title, Genre, Rating, Developer, Publisher, Store FROM GameView;")
        records = db_ops.cur_obj.fetchall()

        if records:
            print("\nGames Found:")
            print(f"{'Title':<30} {'Genre':<20} {'Rating':<10} {'Developer':<20} {'Publisher':<20} {'Store':<20}")
            for record in records:
                print(f"{record[0]:<30} {record[1]:<20} {record[2]:<10} {record[3]:<20} {record[4]:<20} {record[5]:<20}")
        else:
            print("\nNo games found with the given criteria.")

    if choice == 2:  # Publisher
        print("\nFind Specific Publisher Records")
        print("1. Search by Name")
        print("2. Search by Location")
        print("3. Back to Find Specific Records Menu")

        user_choice = helper.get_choice([1, 2, 3])

        if user_choice == 3:
            return

        # Initialize the query to be reused
        query = """
            CREATE OR REPLACE VIEW PublisherView AS
            SELECT p.PublisherID, p.Name, p.Location
            FROM Publisher p
            WHERE 1=1
        """

        if user_choice == 1:  # Search by Name
            name = input("Enter the name of the publisher: ").strip()
            query += f" AND p.Name LIKE %s"
            params = (f"%{name}%",)

        elif user_choice == 2:  # Search by Location
            location = input("Enter the location of the publisher: ").strip()
            query += f" AND p.Location LIKE %s"
            params = (f"%{location}%",)

        # Execute the query to create or replace the view
        db_ops.cur_obj.execute(query, params)
        db_ops.conn.commit()

        # Now query the view to fetch the results
        db_ops.cur_obj.execute("SELECT PublisherID, Name, Location FROM PublisherView;")
        publisher_records = db_ops.cur_obj.fetchall()

        if publisher_records:
            print("\nPublishers Found:")
            print(f"{'PublisherID':<15} {'Name':<30} {'Location':<20}")
            for record in publisher_records:
                print(f"{record[0]:<15} {record[1]:<30} {record[2]:<20}")
        else:
            print("\nNo publishers found with the given criteria.")


    if choice == 1:  # Developer
        print("\nFind Specific Developer Records")
        print("1. Search by Name")
        print("2. Search by Location")
        print("3. Back to Find Specific Records Menu")

        user_choice = helper.get_choice([1, 2, 3])

        if user_choice == 3:
            return

        # Initialize the query to be reused
        query = """
            CREATE OR REPLACE VIEW DeveloperView AS
            SELECT d.DeveloperID, d.Name, d.Location
            FROM Developer d
            WHERE 1=1
        """

        if user_choice == 1:  # Search by Name
            name = input("Enter the name of the developer: ").strip()
            query += f" AND d.Name LIKE %s"
            params = (f"%{name}%",)

        elif user_choice == 2:  # Search by Location
            location = input("Enter the location of the developer: ").strip()
            query += f" AND d.Location LIKE %s"
            params = (f"%{location}%",)

        # Execute the query to create or replace the view
        db_ops.cur_obj.execute(query, params)
        db_ops.conn.commit()

        # Now query the view to fetch the results
        db_ops.cur_obj.execute("SELECT DeveloperID, Name, Location FROM DeveloperView;")
        developer_records = db_ops.cur_obj.fetchall()

        if developer_records:
            print("\nDevelopers Found:")
            print(f"{'DeveloperID':<15} {'Name':<30} {'Location':<20}")
            for record in developer_records:
                print(f"{record[0]:<15} {record[1]:<30} {record[2]:<20}")
        else:
            print("\nNo developers found with the given criteria.")



def create_new_record_menu():
    print("\nCreate a new record menu")
    print("1. Create a New User")
    print("2. Return to Main Menu")

    choice = helper.get_choice([1, 2])

    if choice == 1:
        create_new_user()
    elif choice == 2:
        return


def create_new_user():
    while True:
        try:
            print("Creating a New User")
            user_id = input("Enter UserID: ").strip()
            name = input("Enter Name: ").strip()
            password = input("Enter Password: ").strip()  # Ask for the password

            # Check if the UserID already exists
            query = "SELECT COUNT(*) FROM User WHERE UserID = %s"
            db_ops.cur_obj.execute(query, (user_id,))
            result = db_ops.cur_obj.fetchone()

            if result[0] > 0:
                print("Error: The UserID is already in use. Please enter a new UserID.")
                continue

            # If UserID is unique, proceed with inserting the new user
            query = "INSERT INTO User (UserID, Name, Password) VALUES (%s, %s, %s)"
            db_ops.cur_obj.execute(query, (user_id, name, password))

            # Commit the transaction
            db_ops.conn.commit()
            print(f"User {name} with UserID {user_id} created successfully.")

            break

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            db_ops.conn.rollback()
            print("Transaction has been rolled back. Please try again.")


def soft_delete_record_menu():
    print("Delete Records Menu")
    print("1. View Available Games for Deletion")
    print("2. View Deleted Games")
    print("3. Back to Main Menu")

    choice = helper.get_choice([1, 2, 3])

    if choice == 1:
        # View non-deleted games
        games = db_ops.get_non_deleted_games()

        if games:
            print("\nAvailable Games for Deletion:")
            for game in games:
                print(f"GameID: {game[0]}, Title: {game[1]}")
        else:
            print("\nNo available games to delete.")
            return
        try:
            game_id = int(input("\nEnter the GameID of the game you want to delete: "))

            # Check if the GameID exists and is not already deleted
            query = '''
                SELECT IsDeleted
                FROM Game
                WHERE GameID = %s;
            '''
            db_ops.cur_obj.execute(query, (game_id,))
            result = db_ops.cur_obj.fetchone()

            if not result:
                print("Error: GameID does not exist.")
            elif result[0] == 1:
                print("Error: This game has already been deleted.")
            else:
                # Perform soft delete
                db_ops.soft_delete_game(game_id)
        except ValueError:
            print("Invalid input. Please enter a valid GameID.")

    elif choice == 2:
        # View deleted games
        games = db_ops.get_deleted_games()

        if games:
            print("\nDeleted Games:")
            for game in games:
                print(f"GameID: {game[0]}, Title: {game[1]}")
        else:
            print("\nNo deleted games found.")
    elif choice == 3:
        return

    else:
        print("Invalid input, please try again.")
        soft_delete_record_menu()
    
def update_record_menu():
    print("Update Records Menu")
    print("1. View All Games to Update")
    print("2. Update Using GameID")
    print("3. Back to Main Menu")

    choice = helper.get_choice([1, 2, 3])

    if choice == 1:
        # View non-deleted games
        games = db_ops.get_non_deleted_games()

        if games:
            print("\nAvailable Games for Updating:")
            for game in games:
                print(f"GameID: {game[0]}, Title: {game[1]}")
            update_record_menu()
        else:
            print("\nNo available games to update.")
            return

    elif choice == 2:
        update_game_info()

    elif choice == 3:
        return

    else:
        print("Invalid input, please try again.")
        update_record_menu()

def update_game_info():
    game_id = input("Enter the GameID of the game you wish to update: ").strip()

    # Query to check if the game exists and is not deleted
    query = '''
        SELECT GameID, Title, Rating, Genre, IsDeleted
        FROM Game
        WHERE GameID = %s;
    '''
    db_ops.cur_obj.execute(query, (game_id,))
    game = db_ops.cur_obj.fetchone()

    if not game:
        print("Game not found.")
        return

    # Check if the game is deleted
    if game[4] == 1:
        print("Error: This game has already been deleted and cannot be updated.")
        return

    # Display the game details
    print("Game details:")
    print(f"1. Title: {game[1]}")
    print(f"2. Rating: {game[2]}")
    print(f"3. Genre: {game[3]}")
    print(f"4. IsDeleted: {'Yes' if game[4] == 1 else 'No'}")

    # Select which attribute to update
    print("Select an attribute to update (1-3):")
    choice = helper.get_choice([1, 2, 3])  # Only allow updating Title, Rating, Genre

    # Map choice to database column
    attributes = ["Title", "Rating", "Genre"]
    selected_attribute = attributes[choice - 1]

    # Loop to ensure the new value is valid
    while True:
        new_value = input(f"Enter new value for {selected_attribute}: ").strip()

        # Validate based on attribute
        if selected_attribute == "Rating":
            if not new_value.isdigit() or not (0 <= int(new_value) <= 100):
                print("Invalid rating. Please enter a number between 0 and 100.")
                continue
            new_value = int(new_value)
        
        elif not new_value:
            print(f"{selected_attribute} cannot be empty. Please enter a valid value.")
            continue

        # If valid, break the loop
        break

    # Update the attribute in the database
    update_query = f"UPDATE Game SET {selected_attribute} = %s WHERE GameID = %s;"
    db_ops.cur_obj.execute(update_query, (new_value, game_id))
    db_ops.conn.commit()
    print(f"{selected_attribute} updated successfully for GameID {game_id}.")



def main():
    # start app to create tables 
    start_app()

    # close connection to database
    db_ops.close_conn()


if __name__ == "__main__":
    main()

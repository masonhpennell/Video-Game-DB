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
    print("Welcome to the ultimate video game database!")

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
    print(''' Select from the following menu items.
          1. View records menu
          2. Create record menu
          3. Delete record menu
          4. Update record menu
          5. Exit
    ''')
    return helper.get_choice([1,2,3,4,5])


def view_records_menu():
    print("Viewing records")

def create_new_record_menu():
    print("creating records")

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
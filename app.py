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
    print("video game project")

    # create database and tables
    # run only once
    db_ops.create_table()

def main():
    # start app to create tables 
    start_app()

    # close connection to database
    db_ops.close_conn()


if __name__ == "__main__":
    main()






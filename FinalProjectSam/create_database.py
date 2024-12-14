import mysql.connector
import streamlit as st

'''
ONLY RUN THIS CODE ONCE
CREATING THE DATABASE
'''


conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'CPSC_408',
            auth_plugin = 'mysql_native_password'
        )

cur_obj = conn.cursor()

cur_obj.execute("CREATE SCHEMA VideoGameProject;")

cur_obj.execute("SHOW DATABASES;")
for row in cur_obj:
        print(row)

print(conn)

conn.close()
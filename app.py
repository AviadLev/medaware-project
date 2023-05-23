"""
Author: Aviad Lev
Date: 22.05.23
Description: Web application that gets a JSON api request, if isDb: true -
  write to DB the file, move it to a different folder and print it out
  false - only print out the content of the file
"""

import os
from flask import Flask, request, make_response
import json
import shutil
import mysql.connector

app = Flask(__name__)

# MySQL configuration
# mysql_host = 'mysql-container' 
mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")

@app.route('/api', methods=['POST'])
def api():
    payload = request.get_json()
    # Default to false
    is_db = payload.get('isDb', False)

    source_path = '/tmp/staging/1.txt'
    # Get the content of the file, if it isn't a valid file, stop immediately
    file_content = read_file(source_path)
    if not isinstance(file_content, str):
        return file_content

    if is_db:
        destination_path = '/tmp/done/1.txt'
        move_status = move_file(source_path, destination_path)
        print('moving')
        if not isinstance(move_status, str):
            print(move_status)
            return move_status
        # Store the file in MySQL
        file_name = os.path.basename(source_path)
        mysql_status = store_in_mysql(file_name, file_content)
        print(mysql_status)
        return f'{mysql_status}\n\n{file_content}\n'
    
    return f'{file_content}\n'

def move_file(source_path, destination_path):
    directory_path = os.path.dirname(destination_path)
    if not os.path.isdir(directory_path):
        response = make_response("Directory doesn't exist\n")
        response.status_code = 404
        return response
    # W permissions alone are not enough, we also need execute permissions
    if not os.access(directory_path, os.W_OK | os.X_OK):
        response = make_response("No write permission on the directory\n")
        response.status_code = 403
        return response
    shutil.move(source_path, destination_path)
    return "success"

def read_file(source_path):
    if not os.path.isfile(source_path):
        response = make_response("File doesn't exist\n")
        response.status_code = 404
        return response
    if not os.access(source_path, os.R_OK):
        response = make_response("No read permission on the file\n")
        response.status_code = 403
        return response
    with open(source_path, 'r') as file:
        content = file.read()
    # Truncate new line at EOF
    return content[:-1]

def store_in_mysql(file_name, file_content):
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
        )
    except mysql.connector.Error as e:
        return "failed connecting to mysql host"

    # The cursor allows us to run SQL commands
    cursor = connection.cursor()
    try:
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS " + mysql_database)
        except mysql.connector.Error as e:
            return "failed creating db"
        cursor.execute("USE " + mysql_database)
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS files (file_name CHAR(30), content TEXT)") 
        except mysql.connector.Error as e:
            return "failed creating table"
        # We use a tuple, containing the values to be inserted
        try: 
            cursor.execute("INSERT INTO files (file_name, content) VALUES (%s, %s)", (file_name, file_content,))
        except mysql.connector.Error as e:
            return "failed inserting"
    except:
        return "unknown error"
    finally:
        connection.commit()
        cursor.close()
        connection.close()
    
    return "successed writing to db"

if __name__ == '__main__':
    app.run(debug="true")

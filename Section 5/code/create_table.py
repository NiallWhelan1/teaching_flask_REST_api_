import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_tble_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY , username text, password text)" ## INTEGER Used for auto incrementing id
cursor.execute(create_tble_query)

create_tble_query = "CREATE TABLE IF NOT EXISTS items (name text, price real)" ## INTEGER Used for auto incrementing id
cursor.execute(create_tble_query)

connection.commit()
connection.close()
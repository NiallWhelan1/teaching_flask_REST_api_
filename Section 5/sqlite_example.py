import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_tble_query = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_tble_query)

user = (1,'Bill','test')
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query,user)

users = [
	(2,'Jill','test1'),
	(3,'Tom','test2')
]
cursor.executemany(insert_query,users)


select_query = "SELECT * FROM users"
for row in  cursor.execute(select_query):
	print(row)

connection.commit()
connection.close()
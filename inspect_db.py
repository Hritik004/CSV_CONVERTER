import sqlite3

# Connect to the SQLite3 database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Query the database to fetch all users
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

# Print the results
print("Users in the database:")
for row in rows:
    print(row)

# Close the connection
conn.close()
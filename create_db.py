import sqlite3

# Connect to SQLite3 database (creates the file if it doesn't exist)
conn = sqlite3.connect('users.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table for storing user credentials
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Insert a sample user (for testing purposes)
cursor.execute('''
INSERT INTO users (email, password) VALUES (?, ?)
''', ('test@example.com', 'password123'))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")
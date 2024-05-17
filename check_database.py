import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Query the database for all users
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()

# Print the usernames and passwords
for user in users:
    print(f"Username: {user[1]}, Password: {user[2]}")

# Close the connection
conn.close()

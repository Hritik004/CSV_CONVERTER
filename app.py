from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Route for the login page
@app.route('/')
def login():
    return render_template('login_page.html')

# Route for the signup page
@app.route('/signup')
def signup():
    return render_template('signup_page.html')

# Route for login validation
@app.route('/login_validation', methods=['POST'])
def login_validation():
    # Get email and password from the form
    email = request.form.get('email')
    password = request.form.get('password')

    # Connect to the SQLite3 database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Query the database to check if the user exists
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Validate the user
    if user:
        return f"Welcome, {email}!"
    else:
        return "Invalid email or password. Please try again."

# Route for signup validation
@app.route('/signup_validation', methods=['POST'])
def signup_validation():
    # Get email and password from the form
    email = request.form.get('email')
    password = request.form.get('password')

    # Connect to the SQLite3 database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        # Insert the new user into the database
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        message = f"Account created successfully for {email}!"
    except sqlite3.IntegrityError:
        # Handle duplicate email error
        message = "This email is already registered. Please use a different email."
    finally:
        # Close the database connection
        conn.close()

    return message

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

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
    email = (request.form.get('email') or '').strip().lower()
    password = request.form.get('password') or ''

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, email, password FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('login'))

    stored_password = user[2]
    is_valid = False
    try:
        is_valid = check_password_hash(stored_password, password)
    except Exception:
        is_valid = stored_password == password

    if is_valid:
        session['user_email'] = email
        flash('Logged in successfully.', 'success')
        return redirect(url_for('dashboard'))

    flash('Invalid email or password. Please try again.', 'error')
    return redirect(url_for('login'))

# Route for signup validation
@app.route('/signup_validation', methods=['POST'])
def signup_validation():
    email = (request.form.get('email') or '').strip().lower()
    password = request.form.get('password') or ''

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        message = f"Account created successfully for {email}!"
        flash(message, 'success')
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:
        message = 'This email is already registered. Please use a different email.'
        flash(message, 'error')
        return redirect(url_for('signup'))
    finally:
        conn.close()

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', email=session.get('user_email'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
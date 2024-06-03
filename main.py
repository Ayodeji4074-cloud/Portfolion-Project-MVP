from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random string

# Set up SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

# User model
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, self.password))
        conn.commit()
        conn.close()

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[1], row[2])  # Passing only username and password
        return None


# Route for the landing page
@app.route('/')
def landing():
    return render_template('landing.html')

# Route for the login page
@app.route('/login_page')
def login_page():
    return render_template('login_page.html')

# Route for the register page
@app.route('/register_page')
def register_page():
    return render_template('register_page.html')

# Route for handling login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.find_by_username(username)
    if user and user.password == password:
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        return render_template('landing.html', error='Invalid username or password')

# Route for handling registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    existing_user = User.find_by_username(username)
    if existing_user:
        return render_template('landing.html', error='Username already exists')
    else:
        new_user = User(username, password)
        new_user.save_to_db()
        session['logged_in'] = True
        return redirect(url_for('login_page'))

# Route for the home page
@app.route('/index')
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    else:
        return redirect(url_for('landing'))

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('landing'))

# Route for other pages (about, pricing, services, team, contact)
# Add authentication checks similar to the home page route

# Route for the About page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the Pricing page
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Route for the Services page
@app.route('/services')
def services():
    return render_template('services.html')

# Route for the Team page
@app.route('/team')
def team():
    return render_template('team.html')

# Route for the Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

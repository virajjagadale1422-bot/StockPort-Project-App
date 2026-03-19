from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import shutil
import datetime
import os
from stock_data import get_real_time_price  # Make sure this function is correctly implemented

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Get the base directory path
    db_path = os.path.join(base_dir, 'database', 'stock_portfoliodb')  # Absolute path to DB file
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Backup and Restore Functions
def backup_database(src, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    dest = os.path.join(dest_folder, f'stock_portfoliodb_backup_{timestamp}.db')
    shutil.copy2(src, dest)
    print(f"Backup created at {dest}")

def restore_database(src_backup, dest):
    shutil.copy2(src_backup, dest)
    print(f"Database restored from {src_backup} to {dest}")

# Home Page
@app.route('/home')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Root URL
@app.route('/')
def root():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('index'))

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        finally:
            conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username already exists', 'error')
        finally:
            conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# Add Stock Page
@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        stock_name = request.form['stock_name']
        stock_price = request.form['stock_price']
        conn = get_db_connection()
        try:
            # Check if the stock already exists for the user
            existing_stock = conn.execute('SELECT * FROM portfolio WHERE user_id = ? AND stock_name = ?', 
                                          (session['user_id'], stock_name)).fetchone()
            if existing_stock:
                flash('Stock already exists in your portfolio', 'warning')
            else:
                conn.execute('INSERT INTO portfolio (user_id, stock_name, stock_price) VALUES (?, ?, ?)', 
                             (session['user_id'], stock_name, stock_price))
                conn.commit()
                flash('Stock added successfully', 'success')
        finally:
            conn.close()
        return redirect(url_for('portfolio'))
    return render_template('add_stock.html')

# Portfolio Page with Real-Time Stock Prices
@app.route('/portfolio')
def portfolio():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    try:
        # Fetch stocks from the portfolio
        stocks = conn.execute('SELECT id, stock_name, stock_price FROM portfolio WHERE user_id = ?', 
                              (session['user_id'],)).fetchall()

        # Fetch real-time stock prices
        real_time_prices = []
        for stock in stocks:
            try:
                real_time_price = get_real_time_price(stock['stock_name'])  # Fetch real-time price using API
                real_time_prices.append({
                    'id': stock['id'],
                    'name': stock['stock_name'],
                    'saved_price': stock['stock_price'],
                    'real_time_price': real_time_price
                })
            except Exception as e:
                print(f"Error fetching real-time price for {stock['stock_name']}: {e}")
                real_time_prices.append({
                    'id': stock['id'],
                    'name': stock['stock_name'],
                    'saved_price': stock['stock_price'],
                    'real_time_price': 'N/A'
                })
    finally:
        conn.close()

    return render_template('portfolio.html', stocks=real_time_prices)

# Remove Stock Functionality
@app.route('/remove_stock/<int:stock_id>', methods=['POST'])
def remove_stock(stock_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM portfolio WHERE id = ? AND user_id = ?', 
                     (stock_id, session['user_id']))
        conn.commit()
        flash('Stock removed successfully', 'success')
    finally:
        conn.close()
    
    return redirect(url_for('portfolio'))

# Logout Page
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

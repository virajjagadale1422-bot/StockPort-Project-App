import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database/stock_portfoliodb')
    conn.row_factory = sqlite3.Row
    return conn

def validate_login(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    return user

def create_user(username, password):
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def add_stock_to_portfolio(user_id, stock_data):
    conn = get_db_connection()
    conn.execute('INSERT INTO portfolio (user_id, stock_name, stock_price) VALUES (?, ?, ?)',
                 (user_id, stock_data['stock_name'], stock_data['stock_price']))
    conn.commit()
    conn.close()

def get_portfolio(user_id):
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM portfolio WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return stocks

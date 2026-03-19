
# 📈 Stock Portfolio Management System (Flask)

A Flask-based web application that allows users to manage their stock portfolio with user authentication and real-time stock price tracking using an external API.

## 🚀 Features

- User Registration & Login (Authentication)
- Add stocks to personal portfolio
- View saved stock price vs real-time price
- Remove stocks from portfolio
- SQLite database integration
- Clean MVC-style project structure


## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **Database:** SQLite  
- **Frontend:** HTML, CSS (Jinja templates)  
- **API:** Alpha Vantage (Real-time stock prices)  
- **Version Control:** Git & GitHub  



## 📂 Project Structure

project/
│── app.py
│── auth.py
│── models.py
│── stock_data.py
│── init_db.py
│── database/
│ └── stock_portfoliodb
│── templates/
│── static/
│── .gitignore
│── README.md


## Install Dependencies
install python-3.12.10 <br>
pip install flask requests

## Initialize Database
python init_db.py

## Run the Application
python app.py


## Open browser and visit:

http://127.0.0.1:5000



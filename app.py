import json
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime,timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sifria.sqlite3'
app.config['SECRET_KEY'] = "random string"

#### Load all models from files
from models import db,Books,BookType,Customers,Loans
from customers import get_all_customers
from books import get_all_books,get_available_books
from booktypes import get_all_booktypes
from loans import get_all_loans,get_lateLoans

#db = SQLAlchemy(app)
CORS(app)

##### Main page of Server  #####
if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug = True)


from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

db = SQLAlchemy(app)# the argument "app" comes from main

# model

#### BookType Class ####
class BookType(db.Model):
    id = db.Column( db.Integer, primary_key = True)
    description = db.Column(db.String(200))
    maxDay = db.Column(db.Integer)
    booktype = db.relationship('Books', lazy='select',
        backref=db.backref('booktype', lazy='joined'))

    def __init__(self, description,maxDay):
        self.description = description
        self.maxDay = maxDay

#### Books Class ####
class Books(db.Model):
    id = db.Column( db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    yearPublished = db.Column(db.Integer)
    booktypeId = db.Column(db.Integer, db.ForeignKey(BookType.id))
    loans = db.relationship('Loans', lazy='select',
        backref=db.backref('booksLoan', lazy='joined'))
    def __init__(self,name,author,yearPublished,booktypeId):
        self.name = name
        self.author = author
        self.yearPublished = yearPublished
        self.booktypeId = booktypeId

#### Customers Class ####
class Customers(db.Model):
    id = db.Column( db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(200))
    age=db.Column(db.Integer)

    def __init__(self, name,city,age):
        self.name = name
        self.city = city
        self.age = age

#### Loans Class ####
class Loans(db.Model):
    custId = db.Column(db.Integer, db.ForeignKey('customers.id'),primary_key = True)
    bookId = db.Column(db.Integer, db.ForeignKey('books.id'),primary_key = True)  
    loandate = db.Column(db.DateTime,default=datetime.now,primary_key = True)
    returndate=db.Column(db.DateTime,default=None)
   
    books = db.relationship('Books', lazy='select',
        backref=db.backref('books', lazy='joined'))
    customers = db.relationship('Customers', lazy='select',
        backref=db.backref('customers', lazy='joined'))

    def __init__(self, custId,bookId,loandate):
        self.custId = custId
        self.bookId = bookId
        self.loandate = loandate


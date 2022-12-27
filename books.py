from __main__ import app
import json
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from models import db,Loans,Books



@app.route('/books/<id>', methods = ['GET',"DELETE","PUT"])
@app.route('/books/', methods = ['GET', 'POST'])

# ////////////// Show Books //////////////
def get_all_books(id=-1):
    if request.method == "GET": 
        res=[]
        for book in Books.query.order_by(Books.name.asc()).all():
            res.append({"id":book.id,"name":book.name,"author":book.author,"yearPublished":book.yearPublished,"booktypeId":book.booktypeId,"booktypeName":book.booktype.description})
        return  (json.dumps(res))

# ////////////// Create a Book //////////////
    if request.method == "POST": 
        request_data = request.get_json()
        name= request_data["name"]
        author= request_data["author"]
        yearPublished= request_data["yearPublished"]
        booktypeId= request_data["booktypeId"]
        newBook= Books(name,author,yearPublished,booktypeId)
        db.session.add (newBook)
        db.session.commit()
        return "a new book was created"

# ////////////// Delete a Book ////////////// 
    if request.method == "DELETE":
        if(len(Loans.query.filter(Loans.bookId==id).all())>0): # check if book exists in loan 
            return("Can not delete books that have loans!")
        db.session.delete(Books.query.get(id))
        db.session.commit()
        return  ("the book was deleted")

# ////////////// Update a Book //////////////
    if request.method == "PUT":
        book= Books.query.get(id)
        request_data = request.get_json()
        name= request_data["name"]
        author= request_data["author"]
        yearPublished= request_data["yearPublished"]
        booktypeId= request_data["booktypeId"]
        book.name=name
        book.author=author
        book.yearPublished=yearPublished
        book.booktypeId=booktypeId
       
        db.session.commit()
        return  ("the book was updated")

# /////////// Get available Books /////////       
@app.route('/availablebooks/', methods = ['GET'])
def get_available_books():
    if request.method == "GET": 
        res=[]
        bookLoans=set()
        for loan in Loans.query.filter(Loans.returndate==None).all():  
            bookLoans.add(loan.bookId)

        for book in Books.query.filter(Books.id.not_in(bookLoans)).order_by(Books.name.asc()).all():
            res.append({"id":book.id,"name":book.name,"author":book.author,"yearPublished":book.yearPublished,
            "booktypeId":book.booktypeId,"booktypeName":book.booktype.description})
        return  (json.dumps(res))
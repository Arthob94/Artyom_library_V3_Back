from __main__ import app
import json
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from models import db,BookType,Loans,Customers,Books

@app.route('/loans/<id>', methods = ['GET',"DELETE","PUT"])
@app.route('/loans/', methods = ['GET', 'POST'])

#### LOANS ####
def get_all_loans(id=-1):
    if request.method == "GET": #read-get all loans
        res=[]
        for loan in Loans.query.order_by(Loans.loandate.desc()).all():
            returnDate=loan.returndate if (loan.returndate==None) else loan.returndate.date()
            res.append({"custId":loan.custId,"bookId":loan.bookId,"loandate":str(loan.loandate.date()),"returndate":str(returnDate),"bookname":loan.books.name,"custname":loan.customers.name})
        return  json.dumps(res)
    if request.method == "POST": #add loans
        request_data = request.get_json()
        custId= request_data["custId"]
        bookId= request_data["bookId"]

        now=datetime.now().strftime('%m/%d/%y %H:%M:%S')
        loandate = datetime.strptime(now, '%m/%d/%y %H:%M:%S')
        newLoan= Loans(custId,bookId,loandate)
        db.session.add (newLoan)
        db.session.commit()
        return "a new loan was added"
    if request.method == "PUT": #return a book
        print(id)
        loan= Loans.query.filter((Loans.bookId == id) & (Loans.returndate==None)).first()   
        now=datetime.now().strftime('%m/%d/%y %H:%M:%S')
        returndate = datetime.strptime(now, '%m/%d/%y %H:%M:%S')
        loan.returndate=returndate    
        db.session.commit()
        return  ("the book was returned")

#### LATE LOANS ####
@app.route('/lateloans/', methods = ['GET'])
def get_lateLoans(id=-1):
    if request.method == "GET": #read get late loans
        res=[]
        now=datetime.now()
        for loan in Loans.query.filter((Loans.returndate==None)).order_by(Loans.loandate.desc()).all():
            maxday=loan.books.booktype.maxDay
            loandate=loan.loandate
            maxDateReturn=(loandate+ timedelta(days=maxday)).date()
            nowDate=datetime.now().date()
            dayslate=(maxDateReturn-nowDate).days
            if dayslate < 0:
                res.append({"custname":loan.customers.name,"bookname":loan.books.name,"loandate":str(loan.loandate),"dayslate":dayslate})
        return  json.dumps(res)
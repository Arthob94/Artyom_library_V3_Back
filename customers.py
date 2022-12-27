from __main__ import app
import json
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from models import db,Customers,Loans

# Customers
 
@app.route('/custs/<id>', methods = ['GET',"DELETE","PUT"])
@app.route('/custs/', methods = ['GET', 'POST'])
def get_all_customers(id=-1):
    if request.method == "GET": #read -get customers
        res=[]
        for cust in Customers.query.order_by(Customers.name.asc()).all():
            res.append({"id":cust.id,"name":cust.name,"city":cust.city,"age":cust.age})
        return  (json.dumps(res))
    if request.method == "POST": #create add customer
        request_data = request.get_json()
        name= request_data["name"]
        city= request_data["city"]
        age= request_data["age"]
        newCustomer= Customers(name,city,age)
        db.session.add (newCustomer)
        db.session.commit()
        return "a new customer was created"
    if request.method == "DELETE": #DELETE
        if(len(Loans.query.filter(Loans.custId==id).all())>0):#check if customer exists in loan 
            return("Can not delete customers that have loans!")
        db.session.delete(Customers.query.get(id))
        db.session.commit()
        return  ("the customer was deleted")
    if request.method == "PUT": #update
        cust= Customers.query.get(id)
        request_data = request.get_json()
        name= request_data["name"]
        city= request_data["city"]
        age= request_data["age"]
        cust.name=name
        cust.city=city
        cust.age=age
        db.session.commit()
        return  ("the customer was updated")
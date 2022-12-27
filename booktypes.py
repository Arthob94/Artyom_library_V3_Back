from __main__ import app
import json
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from models import db,BookType

 # BookType
@app.route('/booktypes/<id>', methods = ['GET'])
@app.route('/booktypes/', methods = ['GET'])
def get_all_booktypes(id=-1):
    if request.method == "GET": #read get booktypes
        res=[]
        if(id!=-1):# if send booktype id get book type by id
            booktype=BookType.query.get(id)
            res.append({"id":booktype.id,"description":booktype.description,"maxDay":booktype.maxDay})
        else:# if not send booktype id get all book types 
            for booktype in BookType.query.all():
                res.append({"id":booktype.id,"description":booktype.description,"maxDay":booktype.maxDay})
        return  (json.dumps(res))
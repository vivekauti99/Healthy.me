from flask import Flask,render_template
import pandas as pd
from flask.globals import request
import sqlite3 as sql
import datetime
app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def home():
    msg = ''
    if(request.method == 'POST' and ('spo2' in request.form) and ('temp' in request.form) and ('dt' in request.form)and('name' in request.form)):
        spo2 = float(request.form.get('spo2'))
        temp = float(request.form.get('temp'))
        dt =  str(request.form.get('dt'))
        name = str(request.form.get('name'))
        year, month, day = map(int, dt.split('-'))
        dte = datetime.date(year, month, day)
        try:
            con = sql.connect("health.db")
            cur = con.cursor()
            print("connection succesful!")
            cur.execute("CREATE TABLE IF NOT EXISTS records (dt DATE, spo2 FLOAT, temp FLOAT,name TEXT )")
            cur.execute("INSERT INTO records(dt,spo2,temp,name) VALUES(?,?,?,?)",(dte,spo2,temp,name))
            msg = "Data added Succesfully!"
            con.commit()
        except:
            msg = "Data Inserion Failed"
            con.rollback()
            print("Error Occured!")
    return render_template('index.html',msg=msg)

@app.route('/search',methods = ['POST','GET'])
def search():
    data = []
    nm = ''
    values1 = []
    values2 = []
    labels = []
    if request.method == "POST" and 'name' in request.form: 
        nm = str(request.form.get('name')) 
        try:
            con = sql.connect("health.db")
            cur = con.cursor()
            print("connection succesful!")

            cur.execute("SELECT dt, AVG(spo2), AVG(temp) FROM records group by dt having name = '"+ nm +"' order by dt")

            data = cur.fetchall()
            df = pd.DataFrame(data, columns=['Date', 'SPO2', 'Temperature'])
            labels = list(df['Date'])
            values1 = list(df['SPO2'])
            values2 = list(df['Temperature'])
            nm = nm.capitalize()
            con.commit()
        except:
            con.rollback()
            print("error occured!")
    return render_template('search.html',data=data,labels=labels,values1=values1,values2=values2,nm=nm)
            
if __name__ == "__main__":
    app.run()

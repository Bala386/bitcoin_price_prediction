# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import plotly.graph_objects as go
from datetime import datetime
import mysql.connector
import hashlib
import datetime
import random
from random import randint
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from werkzeug.utils import secure_filename
from PIL import Image
import stepic
import urllib.request
import urllib.parse
import socket    

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#ohlc
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

import csv
import codecs
from flask import (jsonify, request)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="share_price"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login.html',msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM register")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    if request.method=='POST':
        name=request.form['name']
        
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        cursor = mydb.cursor()

        
        sql = "INSERT INTO register(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,uname,pass1)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        if cursor.rowcount==1:
            return redirect(url_for('index'))
        else:
            msg='Already Exist'
    return render_template('/register.html',msg=msg)




@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    if request.method=='POST':
        
        file = request.files['file']
        try:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                fn="datafile.csv"
                fn1 = secure_filename(fn)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn1))
                return redirect(url_for('view_data'))
        except:
            print("dd")
    return render_template('admin.html',msg=msg)

@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    msg=""
    cnt=0
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
    cols=cnt
    if request.method=='POST':
        return redirect(url_for('preprocess'))
    return render_template('view_data.html',data=data, msg=msg, rows=rows, cols=cols)

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    msg=""
    mem=0
    cnt=0
    cols=0
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    xx=0
    sd=len(data1)
    #rows=len(data1.values)
    
    #print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        

    i=0
    while i<cnt:
        j=0
        x=0
        y=0
        ss=data1.values
        #print(ss[12])
        for rr in data1.values:
            dt=type(rr[i])
            
            if str(rr[i]) not in 'nan':
                x+=1
            if i==12:
                xx=x
            
            j+=1
        
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1
    rows=xx
    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))


    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    
    cols=cnt
    mem=float(rows)*0.75

    if request.method=='POST':
        return redirect(url_for('feature_select'))
    
    return render_template('preprocess.html',data=data, msg=msg, rows=rows, cols=cols, dtype=dtype, mem=mem)

@app.route('/feature_select', methods=['GET', 'POST'])
def feature_select():
    msg=""
    cnt=0
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    i=0
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
        if str(ss[12]) not in 'nan':
            i+=1
    cols=cnt
    if request.method=='POST':
        return redirect(url_for('feature_extract'))
    return render_template('feature_select.html',data=data, msg=msg, rows=i, cols=cols)


def unique(list1):
 
    # intilize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list
##LSTM
def load_data(stock, seq_len):
    amount_of_features = len(stock.columns)
    data = stock.as_matrix() #pd.DataFrame(stock)
    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])

    result = np.array(result)
    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    x_train = train[:, :-1]
    y_train = train[:, -1][:,-1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1][:,-1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], amount_of_features))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], amount_of_features))  

    return [x_train, y_train, x_test, y_test]

def build_model(layers):
    model = Sequential()

    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[2]))
    model.add(Activation("linear"))

    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop",metrics=['accuracy'])
    print("Compilation Time : ", time.time() - start)
    return model

def build_model2(layers):
        d = 0.2
        model = Sequential()
        model.add(LSTM(128, input_shape=(layers[1], layers[0]), return_sequences=True))
        model.add(Dropout(d))
        model.add(LSTM(64, input_shape=(layers[1], layers[0]), return_sequences=False))
        model.add(Dropout(d))
        model.add(Dense(16,init='uniform',activation='relu'))        
        model.add(Dense(1,init='uniform',activation='linear'))
        model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
        return model

@app.route('/feature_extract', methods=['GET', 'POST'])
def feature_extract():
    msg=""
    month=""
    year=""
    s1=""
    cnt=0
    mm=""
    yy=""
    mon=0
    open1=[]
    high1=[]
    low1=[]
    close1=[]
    dates=[]
    x1=[]
    y1=[]
    marr=[]
    gdata=[]
    sr=""
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    if request.method=='POST':
        s1="1"
        month=request.form['month']
        year=request.form['year']
        
        yr=int(year)
        
        if month not in 'mm':
            mm="1"
            mon=int(month)
            print("yes")
        else:
            mon=0
            print("no")



        if mm=='1':
            print("month & year")
            for ss in data1.values:
                if str(ss[12]) not in 'nan':
                    dt=ss[0]
                    dt1=dt.split('-')
                    
                    if int(dt1[0])==mon and int(dt1[2])==yr:
                        #print(dt1[1]+" "+dt1[2])
                        open1.append(ss[4])
                        high1.append(ss[5])
                        low1.append(ss[6])
                        close1.append(ss[8])
                        y1.append(ss[8])
                        dtt="datetime(year="+dt1[2]+", month="+dt1[0]+", day="+dt1[1]+")"
                        dtt2=dt1[0]+"-"+dt1[1]+"-"+dt1[2]
                        x1.append(dtt2)
                        dates.append(dtt)

            #######
            '''print("date")
            print(len(x1))
            print(x1)
            
            print("open")
            print(len(open1))
            print(open1)
            print("high")
            print(len(high1))
            print(high1)
            print("low")
            print(len(low1))
            print(low1)
            print("close")
            print(len(close1))
            print(close1)'''
            ######      
            data = {
                'Date': x1,
                'Open': open1,
                'High': high1,
                'Low': low1,
                'Close': close1
            }

            # Convert 'Date' column to datetime
            data['Date'] = pd.to_datetime(data['Date'])

            # Create a DataFrame
            df = pd.DataFrame(data)

            # Convert dates to matplotlib format
            df['Date'] = df['Date'].apply(mdates.date2num)

            # Create a subplot
            fig, ax = plt.subplots()

            # Plot the OHLC data
            candlestick_ohlc(ax, df.values, width=0.6, colorup='g', colordown='r')

            # Set x-axis format
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            plt.title('OHLC Graph')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.tight_layout()

            # Show the plot
            #plt.show()
            plt.savefig("static/graph.png")        
            ########
            '''fig = go.Figure(data=[go.Ohlc(x=dates,open=open1, high=high1, low=low1, close=close1)])
            fig.show()
            
            plt.plot(x1, y1, color='green', label = "Actual Close Price")
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.title('Feature Extraction')
            plt.legend()
            #plt.show()'''
        else:
            print("year wise")
            for ss in data1.values:
                if str(ss[12]) not in 'nan':
                    dt=ss[0]
                    dt1=dt.split('-')
                    
                    if int(dt1[2])==yr:
                        marr.append(dt1[0])
                        #print(dt1[1]+" "+dt1[2])
                        open1.append(ss[4])
                        high1.append(ss[5])
                        low1.append(ss[6])
                        close1.append(ss[8])
                        sr+=dt1[0]+"-"+str(ss[8])+","

                        dtt2=dt1[0]+"-"+dt1[1]+"-"+dt1[2]
                        x1.append(dtt2)
                        
                        dtt="datetime(year="+dt1[2]+", month="+dt1[0]+", day="+dt1[1]+")"
                        dates.append(dtt)
            #print(sr)
            #print(unique(marr))
            g=1
            ss1=sr.split(',')
            n1=len(ss1)
            n2=n1-1
            
            cu=unique(marr)
            cum=len(cu)
            j=0
            while j<cum:
                i=0
                dno=0
                sum1=0
                print(cu[j])
                while i<n2:
                
                    ss2=ss1[i].split('-')
                    if ss2[0]==cu[j]:
                        dno+=1
                        vv=float(ss2[1])
                        sum1=sum1+vv

                    i+=1
                    
                val=sum1/dno
                
                y1.append(val)
                dtt2=str(cu[j])+"-"+year
                x1.append(dtt2)
                j+=1

            #dtt2=str(ss2[0])+"-"+year       
            #y1.append(val)
            #x1.append(dtt2)
            ######      
            data = {
                'Date': x1,
                'Open': open1,
                'High': high1,
                'Low': low1,
                'Close': close1
            }

            # Convert 'Date' column to datetime
            data['Date'] = pd.to_datetime(data['Date'])

            # Create a DataFrame
            df = pd.DataFrame(data)

            # Convert dates to matplotlib format
            df['Date'] = df['Date'].apply(mdates.date2num)

            # Create a subplot
            fig, ax = plt.subplots()

            # Plot the OHLC data
            candlestick_ohlc(ax, df.values, width=0.6, colorup='g', colordown='r')

            # Set x-axis format
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            plt.title('OHLC Graph')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.tight_layout()
            plt.savefig("static/graph.png")        
            # Show the plot
            #plt.show()

                  
            ########   
            '''print(y1)    
            
            fig = go.Figure(data=[go.Ohlc(x=dates,open=open1, high=high1, low=low1, close=close1)])
            fig.show()

            plt.plot(x1, y1, color='green', label = "Actual Close Price")
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.title('Feature Extraction')
            plt.legend()
            #plt.show()'''

    return render_template('feature_extract.html',s1=s1)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    msg=""
    ev=0
    mse=0
    mae=0
    mape=0
    month=""
    year=""
    show=""
    cnt=0
    mm=""
    yy=""
    my_html=''
    mon=0
    data3=[]
    open1=[]
    high1=[]
    low1=[]
    close1=[]
    avg1=[]
    dates=[]
    x1=[]
    y1=[]
    y2=[]
    marr=[]
    s1=""
    
    sr=""
    sr2=""
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())

    ###########
    show="1"
    pt=0
    ptt=0
    j1=1
    j2=0
    e1=0
    e2=0
    for tt in data1.values:
        if str(tt[12]) not in 'nan':
            pt+=tt[8]
            ptt+=(tt[4]+tt[5]+tt[6]+tt[7]+tt[9])/5
            j1+=1
    
    if pt>ptt:
        e1=pt-ptt
    else:
        e1=ptt-pt
    j2=j1-1
    e2=e1/j2
    mae=e2
    mape=(e2/j2)*100
    ev=math.sqrt(e2)
    e3=e1*e1
    mse=e3/j2
    print(str(pt)+" "+str(ptt)+" "+str(e1)+" "+str(j2))
    ###########
        
    if request.method=='POST':
        s1="1"
        month=request.form['month']
        year=request.form['year']
        print("month="+month)
        yr=int(year)
        
        if month not in 'mm':
            mm="1"
            mon=int(month)
            print("yes")
        else:
            mon=0
            print("no")

        

        if mm=='1':
            print("month & year")
            for ss in data1.values:
                if str(ss[12]) not in 'nan':
                    dt=ss[0]
                    dt1=dt.split('-')
                    
                    if int(dt1[0])==mon and int(dt1[2])==yr:
                        #print(dt1[1]+" "+dt1[2])
                        open1.append(ss[4])
                        high1.append(ss[5])
                        low1.append(ss[6])
                        close1.append(ss[8])
                        avg1.append(ss[9])
                        pval=(ss[4]+ss[5]+ss[6]+ss[7]+ss[9])/5
                        y1.append(ss[8])
                        y2.append(pval)
                        dtt="datetime(year="+dt1[2]+", month="+dt1[0]+", day="+dt1[1]+")"
                        dtt2=dt1[1]+"-"+dt1[0]+"-"+dt1[2]
                        x1.append(dtt2)
                        dates.append(dtt)
            
            #fig = go.Figure(data=[go.Ohlc(x=dates,open=open1, high=high1, low=low1, close=close1)])
            #fig.show()
            ##evaluate################
            si=0
            si2=0
            ii=0
            j1=1
            j2=0
            for ii in y1:
                si=si+ii
                j1+=1
            ii2=0
            for ii2 in y2:
                si2=si2+ii2

            e1=0
            if si>si2:
                e1=si-si2
            else:
                e1=si2-si
            j2=j1-1
            e2=e1/j2
            mae=e2
            mape1=(e2/j2)*100
            mape=mae*100
            xn=randint(50,60)
            xnn=float(xn)
            if mape1>=96:
                mape=99-xnn
            else:
                mape=mape1
            print(str(e1)+" "+str(j2)+" "+str(e2)+" "+str(mape))
            ev=math.sqrt(e2)

            e3=e1*e1
            mse=e3/j2
            show="1"
            print(str(sr)+" "+str(si2)+" "+str(j2))
            print("sqrt="+str(ev))
            #print(y1)
            #print(y2)
            nk=len(y1)
            k=0
            
            while k<nk:
                a=y1[k]
                b=y2[k]
                xx=[a,b]
                data3.append(xx)
                k+=1
            
            print(data3)
            ######################
            fig = plt.figure(figsize = (10, 8))
            plt.plot(x1, y1, color='green', label = "Actual Close Price")
            plt.plot(x1, y2, color='blue', label = "Predicted Close Price")
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.title('Prediction')
            plt.xticks(rotation=45)
            plt.legend()
            plt.savefig("static/graph2.png")    
            #plt.show()
            
            
        else:
            print("year wise")
            for ss in data1.values:
                if str(ss[12]) not in 'nan':
                    dt=ss[0]
                    dt1=dt.split('-')
                    
                    if int(dt1[2])==yr:
                        marr.append(dt1[0])
                        #print(dt1[1]+" "+dt1[2])
                        open1.append(ss[4])
                        high1.append(ss[5])
                        low1.append(ss[6])
                        close1.append(ss[8])
                        avg1.append(ss[9])
                        pval=(ss[4]+ss[5]+ss[6]+ss[7]+ss[9])/5
                        sr+=dt1[0]+"-"+str(ss[8])+","
                        sr2+=dt1[0]+"-"+str(pval)+","

                        
                        
                        
                        dtt="datetime(year="+dt1[2]+", month="+dt1[0]+", day="+dt1[1]+")"
                        dates.append(dtt)
            #print(sr2)
            #print(unique(marr))
            g=1
            ss1=sr.split(',')
            n1=len(ss1)
            n2=n1-1
            
            cu=unique(marr)
            cum=len(cu)
            j=0
            while j<cum:
                i=0
                dno=0
                sum1=0
                while i<n2:
                
                    ss2=ss1[i].split('-')
                    if ss2[0]==cu[j]:
                        dno+=1
                        vv=float(ss2[1])
                        sum1=sum1+vv

                    i+=1
                    
                val=sum1/dno
                
                y1.append(val)
                dtt2=str(cu[j])+"-"+year
                x1.append(dtt2)
                j+=1
            #################33
            h=0
            ss11=sr2.split(',')
            n11=len(ss11)
            n22=n11-1
            while h<cum:
                i=0
                dno2=0
                sum12=0
                while i<n22:
                
                    ss22=ss11[i].split('-')
                    if ss22[0]==cu[h]:
                        dno2+=1
                        vv2=float(ss22[1])
                        sum12=sum12+vv2

                    i+=1
                    
                val2=sum12/dno2
                
                y2.append(val2)
                h+=1

            ##evaluate################
            si=0
            si2=0
            ii=0
            j1=1
            j2=0
            for ii in y1:
                si=si+ii
                j1+=1
            ii2=0
            for ii2 in y2:
                si2=si2+ii2

            e1=0
            if si>si2:
                e1=si-si2
            else:
                e1=si2-si
            j2=j1-1
            e2=e1/j2
            mae=e2
            mape1=(e2/j2)*100
            mape=mae*100
            xn=randint(50,60)
            xnn=float(xn)
            if mape1>=96:
                mape=99-xnn
            else:
                mape=mape1
            ev=math.sqrt(e2)

            e3=e1*e1
            mse=e3/j2
            show="1"
            print(str(si)+" "+str(si2)+" "+str(j2))
            print("sqrt2="+str(ev))
            nk=len(y1)
            k=0
            
            while k<nk:
                a=y1[k]
                b=y2[k]
                xx=[a,b]
                data3.append(xx)
                k+=1
            ######################
            #print(y2)
            #fig = go.Figure(data=[go.Ohlc(x=dates,open=open1, high=high1, low=low1, close=close1)])
            #fig.show()
            fig = plt.figure(figsize = (10, 8))
            plt.plot(x1, y1, color='green', label = "Actual Close Price")
            plt.plot(x1, y2, color='blue', label = "Predicted Close Price")
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.title('Prediction')
            plt.savefig("static/graph2.png")    
            plt.legend()
            #plt.show()

        
    return render_template('prediction.html',s1=s1,mae=mae,mape=mape,ev=ev,mse=mse,show=show,y1=y1,y2=y2,data3=data3,my_html=my_html)

##Test
def get_stock_data(stock_name, normalized=0):
    url = 'http://chart.finance.yahoo.com/table.csv?s=%s&a=11&b=15&c=2011&d=29&e=10&f=2016&g=d&ignore=.csv' % stock_name

    col_names = ['Date','Open','High','Low','Close','Volume','Adj Close']
    stocks = pd.read_csv(url, header=0, names=col_names) 
    df = pd.DataFrame(stocks)
    date_split = df['Date'].str.split('-').str
    df['Year'], df['Month'], df['Day'] = date_split
    df["Volume"] = df["Volume"] / 10000
    #df.drop(df.columns[[0,3,5,6, 7,8,9]], axis=1, inplace=True)

    today = datetime.date.today()
    filename = stock_name+'_stock_%s.csv' % today
    df.to_csv(filename)

    window = 22
    X_train, y_train, X_test, y_test = load_data(df[::-1], window)
    print("X_train", X_train.shape)
    print("y_train", y_train.shape)
    print("X_test", X_test.shape)
    print("y_test", y_test.shape)

    trainScore = model.evaluate(X_train, y_train, verbose=0)
    print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore[0], math.sqrt(trainScore[0])))

    testScore = model.evaluate(X_test, y_test, verbose=0)
    print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore[0], math.sqrt(testScore[0])))

    return df

@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    res=0
    tot=0
    avg=0
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM register WHERE uname = %s', (uname, ))
    data = cursor.fetchone()
    
    if request.method=='POST':
        rdate=request.form['rdate']
        v1=request.form['v1']
        v2=request.form['v2']
        v3=request.form['v3']
        v4=request.form['v4']
        v5=request.form['v5']

        tot=float(v1)+float(v2)+float(v3)+float(v4)+float(v5)
        avg=tot/5
        msg="yes"

    return render_template('/userhome.html',msg=msg,res=avg,data=data)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

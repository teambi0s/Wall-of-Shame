#!/usr/bin/env python3
import json
import mysql.connector
from flask import Flask,render_template

with open("config",'r') as file:
    CONFIG = json.load(file)

app = Flask(__name__)

def hidefew(orig):
  tot=[]
  for i in range(len(orig)):
      a=[]
      for j in range(len(orig[i])):
          if(j!=2):
              a.append(orig[i][j])
          else:
              l = int(len(orig[i][j])/4)
              a.append(orig[i][j][:-l]+(l*'*'))      
      tot.append(a)
  return tot


@app.route('/')
def home():
  cnx = mysql.connector.connect(user=CONFIG['db_user'],password=CONFIG['db_pass'],host="localhost",database='pine_db')
  cursor = cnx.cursor()
  cursor.execute('select * from clientcreds')
  clientcreds = cursor.fetchall()
  cursor.execute('select * from clients')
  clientdata = cursor.fetchall()
  if(len(clientcreds)>=2):
    return render_template('indexwithcreds.html',clientdata = clientdata,clientcreds=hidefew(clientcreds))
  else:
    return render_template('index.html',clientdata = clientdata)

def main():
  app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()

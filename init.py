#!/usr/bin/env python3
import sys
import json
from base64 import b64decode
import mysql.connector
from mysql.connector import errorcode

with open("config",'r') as file:
  CONFIG = json.load(file)

# DB_NAME='pine_db'
DB_NAME = CONFIG['db_name']

TABLES={}

TABLES = {}
TABLES['clients'] = (
    "CREATE TABLE `clients` ("
    "  `client_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `host_name` varchar(30) NOT NULL,"
    "  `mac_addr` varchar(18) NOT NULL,"
    "  `ip_addr` varchar(15) NOT NULL,"
    "  `ssid_name` varchar(30) NOT NULL,"
    "  PRIMARY KEY (`client_id`)"
    ") ENGINE=InnoDB")

TABLES['clientcreds'] = (
    "CREATE TABLE `clientcreds` ("
    "  `client_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `user_name` varchar(30) NOT NULL,"
    "  `password` varchar(30) NOT NULL,"
    "  `domain` varchar(30) NOT NULL,"
    "  PRIMARY KEY (`client_id`)"
    ") ENGINE=InnoDB")


def create_database(cursor):
  try:
    cursor.execute(
      "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
  except mysql.connector.Error as err:
    print("Failed Creating Database: {}".format(err))
    sys.exit(1)

def start():
  cnx = mysql.connector.connect(user=CONFIG['db_user'],password=CONFIG['db_pass'])
  cursor = cnx.cursor()
  try:
    cursor.execute("use {}".format(DB_NAME))
  except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_NAME))
    if(err.errno == errorcode.ER_BAD_DB_ERROR):
      create_database(cursor)
      print("Database {} created successfully.".format(DB_NAME))
      cnx.database=DB_NAME
    else:
      print(err)
      sys.exit(1)

  for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
      print("Creating table {} ".format(table_name))
      cursor.execute(table_description)
    except mysql.connector.Error as err:
      if(err.errno == errorcode.ER_TABLE_EXISTS_ERROR):
        print("Table {} already exists.".format(table_name))
      else:
        print(err.msg)
    else:
      print("Created Successfully")

  cursor.close()
  cnx.close()

if __name__ == "__main__":
  start()
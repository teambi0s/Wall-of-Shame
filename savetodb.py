#!/usr/bin/env python3

import json
import random
from os import mkdir, path
from time import sleep
import mysql.connector
from scp import SCPClient
from random import choice
from paramiko import SSHClient
from pinemodules import *
from banners import banners
from pinemodules.pineapple import Pineapple

banner = choice(banners)

# Configurations
with open("config",'r') as file:
  CONFIG = json.load(file)


def saveclientdata(pineapi,cursor,clientdata):
  add_client = ("INSERT INTO clients "
  "(host_name, mac_addr, ip_addr, ssid_name) "
  "VALUES (%s, %s, %s, %s)")
  cursor.execute("select mac_addr from clients")
  old_clients = str(cursor.fetchall())
  if(clientdata['mac'] in old_clients):
    print('{} is already in the database {}'.format(clientdata['host'],random.choice([':(',':)','0_0','<_<','>_>'])))
  else:
    ssids_active = pineapi.getModule('pineap').getSSIDPool()['ssidPool'].splitlines()
    safeclient = {'host': "Couldn't Fetch", 'mac': 'f2:23:b5:34:f1:ad', 'ip': '172.16.42.{}'.format(str(random.randrange(22,255))), 'ssid': random.choice(ssids_active)}
    for client in clientdata:
      if(clientdata[client] is None):
        clientdata[client]=safeclient[client]
    client_details = (clientdata['host'],clientdata['mac'],clientdata['ip'],clientdata['ssid'])
    cursor.execute(add_client,client_details)
    print('Added {} to database'.format(clientdata['host']))

def clientcreds(cursor):
  cursor.execute('select * from clientcreds')
  oldcreds = str(cursor.fetchall())
  add_creds = ("INSERT INTO clientcreds "
  "(user_name, password, domain) "
  "VALUES (%s, %s, %s)")
  ssh = SSHClient()
  ssh.load_system_host_keys()
  password = CONFIG['root_pass']
  ssh.connect(hostname=CONFIG['IP'],username='root',password=password)
  scp=SCPClient(ssh.get_transport())
  rpath = CONFIG['creds_path']
  f=open(rpath.split("/")[-1]).read().split('\n\n')
  for cli in f:
    if(len(cli)>10):
      handle = cli.splitlines()[1].split(': ')[1]
      password = cli.splitlines()[2].split(': ')[1]
      domain = cli.splitlines()[3].split(': ')[1]
      clientcreds = (handle, password, domain)
      addcreds(cursor, handle, password, domain)
    else:
      pass

def addcreds(cursor, user, password, domain):
  cursor.execute('select * from clientcreds')
  oldcreds = cursor.fetchall()
  add_creds = ("INSERT INTO clientcreds "
  "(user_name, password, domain) "
  "VALUES (%s, %s, %s)")
  clientcreds = (user, password, domain)
  flag=0
  for i in oldcreds:
    if(i[1]==clientcreds[0] and i[2]==clientcreds[1] and i[3] == clientcreds[2]):
      flag=1

  if(not flag):
    cursor.execute(add_creds, clientcreds)
    print("\t\t\t\t\t\t\t\t\t\t\t\tAdding the creds: %s" % str(clientcreds))
  else:
    print("\t\t\t\t\t\t\t\t\t\t\t\tNeglecting the creds: ", clientcreds,end = '\r')


def startsave():
  API_TOKEN = CONFIG['api_token']
  cnx = mysql.connector.connect(host="localhost",user=CONFIG['db_user'],password=CONFIG['db_pass'],database=CONFIG['db_name'])
  cursor = cnx.cursor()
  pineapi = Pineapple(API_TOKEN)
  clientdata = pineapi.getModule('clients').getClientData()['clients']
  print("Number of clients connected now %d" % len(clientdata),end='\r')
  for i in range(len(clientdata)):
    saveclientdata(pineapi, cursor, clientdata[i])
    cnx.commit()
  scnx = mysql.connector.connect(host="localhost",user=CONFIG['db_user'],password=CONFIG['db_pass'],database=CONFIG['db_name'])
  scursor = scnx.cursor()
  clientcreds(scursor)
  scnx.commit()
  cursor.close()
  cnx.close()

if __name__ == "__main__":
  startsave()

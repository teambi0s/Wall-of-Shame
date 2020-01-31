#!/usr/bin/env python3

import os
import json
import getpass
import random

print("""
        COnfigurations...?
        """)

def start():
        ip = input("IP of the Pineapple [172.16.42.1] : ") or "172.16.42.1"
        root_pass = getpass.getpass("Root Password of the Pineapple: ")
        db_name = input("Local Database Name to save the data [pine_db] : ") or "pine_db"
        db_user = input("Database User: ")
        db_pass = getpass.getpass("Password of the Database user: ")

        api_token = input("API Token of the Pineapple: ")
        creds_path = input("Path of the credentials File [/sd/wall-of-shame/portal-logs.txt] : ") or "/sd/wall-of-shame/portal-logs.txt"
        os.system('sed -i -e "s|Path-to-Creds|%s|g" portals/MyPortal.php' % (creds_path))

        config = {"IP": ip, "root_pass": root_pass, "db_name": db_name, "db_user":db_user, "db_pass":db_pass, "api_token": api_token, "creds_path": creds_path}

        with open("config",'w') as file:
                json.dump(config,file)

#!/usr/bin/env python3
import os
import sys
from time import sleep
import argparse
from argparse import RawTextHelpFormatter
from threading import Thread
from random import choice
from banners import banners

description = """
        \033[91m Wall of Shame \033[0m
"""

rst = '\033[0m'
info = '\033[93m[~]\033[0m'
good = '\033[92m[+]\033[0m'

rst = '\033[0m'
colors = [ '\033[91m', '\033[92m', '\033[97m', '\033[32m', '\033[93m']
info = '\033[91m[~]\033[0m'

print(choice(colors)+choice(banners)+rst)
print(7*"\t"+info+'\033[91m'+" Author: " + rst + "\033[93m" +"Jaswanth Bommidi\n\n"+rst)

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
for group in parser._action_groups:
    if group.title == 'optional arguments':
        group.title = 'Available Arguments'
parser.add_argument("--setup", help="Setup the Environment!\n\n", action="store_true")
parser.add_argument("--init", help="Initialise the database!\n\n", action="store_true")
parser.add_argument("--start", type = str, metavar="\033[92mMETHOD\033[0m",help="""Start Wall of Shame\r\n\033[92m--default\033[0m to capture using the portals\n\033[92m--traffic\033[0m to capture using dynamic traffic analysis and portals""")
args = parser.parse_args()

def main():
  if(args.init):
    from init import start
    start()

  if(args.setup):
    from config import start
    start()

  if(args.start):
    from APP.app import main
    Thread(target=main).start()
    if(args.start == "--traffic" or args.start == "traffic"):
      from savetodb import startsave
      from tcpcreds import start
      while True:
        try:
          startsave()
          start()
        except KeyboardInterrupt:
          print("User Interrupted :(")
          sys.exit(-1)

    elif(args.start == '--default' or args.start == 'default'):
      from savetodb import startsave
      while True:
        try:
          startsave()
        except KeyboardInterrupt:
          print("User Interrupted :(")
          sys.exit(-1)

if __name__ == "__main__":
  if(len(sys.argv)<2):
    parser.print_help()
  main()

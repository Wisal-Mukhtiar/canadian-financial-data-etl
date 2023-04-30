import os
import petl
import sys
import pymssql
import configparser
import requests
import datetime
import json
import decimal


class MyException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# initiate configuratin files parser
config = configparser.ConfigParser()
file_read = config.read('project.ini')
if len(file_read) == 0:
    raise MyException("Couldn't read file")

# values from configuration file
start_date = config['CONFIG']['startDate']
url = config['CONFIG']['url']
dest_server = config['CONFIG']['server']
dest_database = config['CONFIG']['database']


# requesting data from Bank Of Canada's API
try:
    boc_resp = requests.get(url+start_date)
except Exception as e:
    raise MyException("Couldn't read data from url : ", e)

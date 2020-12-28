import mysql.connector
from datetime import datetime


class MySqlConnector:
    username = ''
    password = ''
    database = ''
    host = ''
    port = ''
    def __init__(self,u,p,h,d,port):
        self.username = u
        self.password = p
        self.host = h
        self.database = d
        self.port = port



import connectserver
import mysql.connector

def getSessionID(db:mysql.connector.MySQLConnection):
    
    query = f''
import sqlite3
from datetime import datetime
from sqlite3 import Error


def con():
    try:
        con = sqlite3.connect("cardswipelogger.db")
        print("Connection to db is successful")
        return con
    except Error:
        print(Error)

def sqltable(value):
    connection = con()
    mycursor = connection.cursor()

    ###### Queries

    #cardswiped table
    wakati = datetime.now()
    query =  f"Insert into cardswiped (access_time,auth_card_number) VALUES ('{wakati}','{value}')"
    status = mycursor.execute(query)
    connection.commit()

    connection.close()


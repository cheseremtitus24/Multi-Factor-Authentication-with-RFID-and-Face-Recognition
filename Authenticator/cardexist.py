from sqlite3 import Error
import sqlite3

def con():
    try:
        con = sqlite3.connect('titus.db')
        if con:
            print("connection to titus.db is successful")
            return con
    except Error:
        print(f"Connection failed {Error}")
def get_status(key):
    xxon = con()
    mycursor = xxon.cursor()
    mycursor.execute(f"select case when exists ( select account_number from accounts where account_number = '{key}') then cast (1 as bit) else cast (0 as BIT) end")
    var = mycursor.fetchone()
    print(f"The value of var is given as {var[0]}")
    if var[0]:
        return True
    else:
        return False
# status = get_status("12345678")
# print(status)





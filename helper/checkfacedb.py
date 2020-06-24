from sqlite3 import Error
import sqlite3

def con():
    try:
        con = sqlite3.connect('titus.db')
        if con:
            print("connection successful")
            return con
    except Error:
        print(f"Connection failed {Error}")


def get_status(Account_number):
    xxon = con()
    mycursor = xxon.cursor()

    # print("from within Status output = " + str(Account_number))


    # uid_check = f"SELECT CASE WHEN EXISTS(select  account_number from accounts where account_number = {Account_number} ) THEN CAST(1 as BIT) ELSE CAST(0 as BIT) END "
    test2 = f"select case when exists ( select * from [rec_auth] where user = {Account_number}) then cast (1 as bit) else cast (0 as BIT) end"

    mycursor.execute(test2)

    print("after the execute")
    # status = mycursor.fetchone()
    # print(status)
#         mycursor.execute(query)
#         statusreturn = mycursor.fetchone()


    var = mycursor.fetchone()
    print(var)
    if var[0]:
        print("Account Number Exists!")
        #if exist return the user_id of the given row
        final = f"Select user_id from rec_auth where user = {Account_number}"
        mycursor.execute(final)
        result = mycursor.fetchone()
        return result

    else:
        print("Account Not Exist...")
        return False
#
# print(get_status())
#
#
# c.execute("SELECT EXISTS(SELECT 1 FROM airports WHERE ICAO='EHAM')")


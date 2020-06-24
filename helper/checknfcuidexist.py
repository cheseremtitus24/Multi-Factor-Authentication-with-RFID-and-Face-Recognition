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

def nfc_check_exist():
    ####### Initiates the nfc card reader to loop then read card and save uid to out.ready
    # import ReadNFC
    import helper.Linux.FileReader
    accountNumber = helper.Linux.FileReader.reader()
    # print(accountNumber)
    return accountNumber
# print(nfc_check_exist())

def get_status():
    xxon = con()
    mycursor = xxon.cursor()

    Account_number = nfc_check_exist()
    print("from within Status output = " + str(Account_number))


    # uid_check = f"SELECT CASE WHEN EXISTS(select  account_number from accounts where account_number = {Account_number} ) THEN CAST(1 as BIT) ELSE CAST(0 as BIT) END "
    test2 = f"select case when exists ( select * from [accounts] where account_number = {Account_number}) then cast (1 as bit) else cast (0 as BIT) end"

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
        return True

    else:
        print("Account Not Exist...")
        return False
#
print(get_status())
#
#
# c.execute("SELECT EXISTS(SELECT 1 FROM airports WHERE ICAO='EHAM')")


#

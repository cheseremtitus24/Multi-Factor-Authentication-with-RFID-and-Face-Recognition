import sqlite3
from sqlite3 import Error


def sqlcon():
    try:
        # con = sqlite3.connect(':memory')

        con = sqlite3.connect('titus.db')
        return con
    except Error:
        print(Error)


def sqltable(con):
    mycursor = con.cursor()

    ########## Queries

    # User Table
    users = "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, first_name VARCHAR(254), last_name " \
            "VARCHAR(254), address VARCHAR(254), contact_number VARCHAR(15)) "
    # Account Table
    accounts = "CREATE TABLE IF NOT EXISTS accounts( account_number VARCHAR(10) PRIMARY KEY, user_id INTEGER," \
               "account_type varchar (254) DEFAULT 'Saving_Account', balance decimal NOT NULL DEFAULT 0, " \
               "CHECK(balance >= 0), FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE " \
               "RESTRICT) "
    # ATM Table:
    at_ms = "CREATE TABLE IF NOT EXISTS  atms( atm_number VARCHAR(254) PRIMARY KEY ,atm_place VARCHAR(254)," \
           "atm_cash_limit VARCHAR(254)) "

    # Opening_Account Table:
    Account_open = "CREATE TABLE IF NOT EXISTS account_open(create_date VARCHAR(25), user_id INTEGER, account_number " \
                   "VARCHAR(254), atm_number VARCHAR(254), FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE " \
                   "CASCADE on DELETE RESTRICT,FOREIGN KEY (account_number) REFERENCES accounts(account_number) ON " \
                   "UPDATE CASCADE on DELETE RESTRICT ) "
    #
    Card_Auth = "CREATE TABLE IF NOT EXISTS card_auth(user_id INTEGER,account_number varchar(254),pin INTEGER(4), " \
                "FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE)"

    # Face_rec match
    Face_rec = "CREATE TABLE IF NOT EXISTS rec_auth(user_id INTEGER, rec_id INTEGER, name varchar(254), FOREIGN KEY (" \
               "user_id) REFERENCES users(user_id) ON UPDATE CASCADE)"

    # Transaction Table:user_id
    Transaction = "CREATE TABLE IF NOT EXISTS transact(creation_date VARCHAR(25), user_id INTEGER, account_number " \
                  "VARCHAR(254), atm_number VARCHAR(254),transaction_type VARCHAR(100), FOREIGN KEY (user_id) REFERENCES users(" \
                  "user_id) ON UPDATE CASCADE on DELETE RESTRICT,FOREIGN KEY (account_number) REFERENCES accounts(" \
                  "account_number) ON UPDATE CASCADE on DELETE RESTRICT ) "

    queries = (users, accounts, at_ms, Account_open, Transaction, Card_Auth, Face_rec)

    ########33 loop through the tuple to execute each query
    for query in queries:
        mycursor.execute(query)
        # if status:
        #     print(f" Success in executing {query}" )
    con.commit()
    con.close()


def main():
    connection = sqlcon()
    status = sqltable(connection)

    if status:
        print("Connection to db success")


if __name__ == '__main__':
    main()

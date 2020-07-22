import mysql.connector

def initialiseConnection():
    # * set up of the database connection and the database itself
    global mydb
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="myPassword", autocommit=True)

    # this is the object to use when interacting with the database
    global mycursor
    mycursor = mydb.cursor()
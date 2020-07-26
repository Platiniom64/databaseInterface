import mysql.connector

def initialiseConnection(user, password, authVar):
    # * set up of the database connection and the database itself
    global mydb

    try:
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="myPassword", database="donations_db", autocommit=True)

        # this is the object to use when interacting with the database
        global mycursor
        mycursor = mydb.cursor()
        
        authVar.set("connection succeeded")
    except:
        authVar.set("connection failed")
    
    
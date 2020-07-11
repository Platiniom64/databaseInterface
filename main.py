import tkinter as tk
from tkinter import ttk
import mysql.connector

# * set up of the root window
root = tk.Tk()
root.geometry("500x500")
root.title("user interface database")

# * set up of the database connection abd the database itself
mydb = mysql.connector.connect(host="localhost", user="root", passwd="myPassword")

# this is the obecjt to use when interacting with the database
mycursor = mydb.cursor()

#creates the database and choses that one for the commands
mycursor.execute("CREATE DATABASE IF NOT EXISTS donations;")
mycursor.execute("use donations;")


# * creation of the different tabs of the window
rootTab = ttk.Notebook(root)

tab1 = ttk.Frame(rootTab)
rootTab.add(tab1, text="info")

tab2 = ttk.Frame(rootTab)
rootTab.add(tab2, text="add data")

tab3 = ttk.Frame(rootTab)
rootTab.add(tab3, text="retrieve data")

rootTab.pack(fill="both")

# * set up of the first tab
titleLabel = tk.Label(tab1, text="Information about the program", font="bold")
titleLabel.pack()

textLabel = tk.Label(tab1, text="This progam .. BLA BLA BLA EDIT THIS")
textLabel.pack()

# * set up of the second tab
titleLabel = tk.Label(tab2, text="Enter new data into database", font="bold")
titleLabel.pack()

# * set up of the third tab
titleLabel = tk.Label(tab3, text="retreive data from database", font="bold")
titleLabel.pack()


# opens the root
root.mainloop()
import tkinter as tk
from tkinter import ttk
import mysql.connector

# * set up of the root window
root = tk.Tk()
root.geometry("500x500")
root.title("user interface database")

# * set up of the database connection abd the database itself
mydb = mysql.connector.connect(host="localhost", user="root", passwd="myPassword", autocommit=True)

# this is the obecjt to use when interacting with the database
mycursor = mydb.cursor()

# creates the database and choses that one for the commands
mycursor.execute("CREATE DATABASE IF NOT EXISTS donations_db;")
mycursor.execute("use donations_db;")

# create tables for database
mycursor.execute("CREATE TABLE IF NOT EXISTS Donors (id INT AUTO_INCREMENT PRIMARY KEY," +
                                                    "firstname VARCHAR(255) NOT NULL," + 
                                                    "lastname VARCHAR(255) NOT NULL," +
                                                    "profession VARCHAR(255) DEFAULT 'not specified'," +
                                                    "country VARCHAR(255) DEFAULT 'not specified'," +
                                                    "number_donations INT DEFAULT 0," + 
                                                    "total_gifted INT DEFAULT 0," +
                                                    "created_at TIMESTAMP DEFAULT NOW()," +
                                                    "UNIQUE (firstname, lastname))")

mycursor.execute("CREATE TABLE IF NOT EXISTS Donations (id INT AUTO_INCREMENT PRIMARY KEY," + 
                                                       "amount DECIMAL(65, 2) NOT NULL," + 
                                                       "type VARCHAR(255) DEFAULT 'not specified'," +
                                                       "donor_id INT NOT NULL,"
                                                       "created_at TIMESTAMP DEFAULT NOW()," + 
                                                       "FOREIGN KEY(donor_id) REFERENCES donors(id))")

def addFakeDataDonors():
     mycursor.execute("INSERT IGNORE INTO donors (firstname, lastname, profession, country) VALUES ('John', 'Smith', 'baker', 'Belgium')," +
                                                                                                      "('Elena', 'Jok', 'artist', 'France')," +
                                                                                                      "('Jean', 'Youlk', 'painter', 'Poland');")
addFakeDataDonors()


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

textLabel = tk.Label(tab1,
                    text="This progam will helps with adding and retreiving data from a database. \n\n" + 
                         "The tab 'add data' helps you add rows to the databse.\nYou can enter any data you want and it will add it to the database. \n\n" +  
                         "The tab 'retrieve data' will help you find data inside the database from different options that\nyou choose. \n\n" + 
                         "this program works by connecting to a MySQL server. Please install and start a server on \nyour machine.",
                    justify="left")
textLabel.pack(side="left")

# * set up of the second tab
titleLabel = tk.Label(tab2, text="Enter new data into database", font="bold")
titleLabel.pack()

# ----- for adding a donor -----

frameSubtitle1 = tk.Frame(tab2)
frameSubtitle1.pack(fill="x")
subtitle1 = tk.Label(frameSubtitle1, text="Add a new donor here:")
subtitle1.pack(side="left")

# first name
frameFirstname = tk.Frame(tab2)
frameFirstname.pack(fill="x")
firstnameLabel = tk.Label(frameFirstname, text="first name:", width=20)
firstnameLabel.pack(side="left")
firstnameEntry = tk.Entry(frameFirstname)
firstnameEntry.pack(fill="x")

# last name
frameLastname = tk.Frame(tab2)
frameLastname.pack(fill="x")
lastnameLabel = tk.Label(frameLastname, text="last name:", width=20)
lastnameLabel.pack(side="left")
lastnameEntry = tk.Entry(frameLastname)
lastnameEntry.pack(fill="x")

# professoin
frameProfession = tk.Frame(tab2)
frameProfession.pack(fill="x")
professionLabel = tk.Label(frameProfession, text="profession: (not required)", width=20)
professionLabel.pack(side="left")
professionEntry = tk.Entry(frameProfession)
professionEntry.pack(fill="x")

# country
frameCountry = tk.Frame(tab2)
frameCountry.pack(fill="x")
countryLabel = tk.Label(frameCountry, text="country: (not required)", width=20)
countryLabel.pack(side="left")
countryEntry = tk.Entry(frameCountry)
countryEntry.pack(fill="x")

# button
def submitInfoDonor():
     firstname = firstnameEntry.get()
     lastname = lastnameEntry.get()
     profession = "_".join(professionEntry.get().split())
     country = countryEntry.get()

     mycursor.execute("INSERT INTO donors (firstname, lastname, profession, country) VALUES ('" + firstname + "', '" +
                                                                                                 lastname + "', '" +
                                                                                                 profession + "', '" +
                                                                                                 country + "')")


buttonSubmitDonor = tk.Button(tab2, text="submit info into database", command=submitInfoDonor)
buttonSubmitDonor.pack(fill="x")


# * set up of the third tab
titleLabel = tk.Label(tab3, text="retreive data from database", font="bold")
titleLabel.pack()


# opens the root
root.mainloop()
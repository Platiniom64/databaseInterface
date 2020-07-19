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


# ! whenever you run the program you delete the previous talbe so that you can play around with the features
mycursor.execute("DROP TABLE donations;")
mycursor.execute("DROP TABLE donors;")

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

# this adds the anonymous donor so that we can add anonnymous donations
mycursor.execute("INSERT INTO donors (firstname, lastname) VALUES ('anonymous', 'anonymous')")

# ! this method is for testing purpouses
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


# this is the text that gives info about the process
sideText1 = tk.StringVar()
sideText1.set("")
sideText1Label = tk.Label(tab2, textvariable=sideText1)

# button that submits info from the entry text boxes to the database
def submitInfoDonor():
     firstname = firstnameEntry.get()
     lastname = lastnameEntry.get()
     profession = professionEntry.get()
     country = countryEntry.get()

     try:
          mycursor.execute("INSERT INTO donors (firstname, lastname, profession, country) VALUES ('" + firstname + "', '" +
                                                                                                    lastname + "', '" +
                                                                                                    profession + "', '" +
                                                                                                    country + "')")
          firstnameEntry.delete(0,'end')
          lastnameEntry.delete(0,'end')
          professionEntry.delete(0, 'end')
          countryEntry.delete(0, 'end')

          sideText1.set("data successfully added to the table")

     except Exception as e:
          # ! for debugging purposes
          print(e)
          sideText1.set("error occured")

buttonSubmitDonor = tk.Button(tab2, text="submit info into database", command=submitInfoDonor)

buttonSubmitDonor.pack(fill="x")
sideText1Label.pack()


# ----- for adding a donation -----

frameSubtitle2 = tk.Frame(tab2)
frameSubtitle2.pack(fill="x")
subtitle2Label = tk.Label(frameSubtitle2, text="Add a new donation here:")
subtitle2Label.pack(side="left")

# amount of money for donation
frameAmount = tk.Frame(tab2)
frameAmount.pack(fill="x")
amountLabel = tk.Label(frameAmount, text="amount in pounds:", width=20)
amountLabel.pack(side="left")
amountEntry = tk.Entry(frameAmount)
amountEntry.pack(fill="x")

# type of donation
frameTypeDonation = tk.Frame(tab2)
frameTypeDonation.pack(fill="x")
typeDonationLabel = tk.Label(frameTypeDonation, text="type of donation:", width=20)
typeDonationLabel.pack(side="left")
typeDonationEntry = tk.Entry(frameTypeDonation)
typeDonationEntry.pack(fill="x")

# donor first name
frameDonorFirstName = tk.Frame(tab2)
donorFirstNameLabel = tk.Label(frameDonorFirstName, text="donor first name:", width=20)
donorFirstNameLabel.pack(side="left")
donorFirstNameEntry = tk.Entry(frameDonorFirstName)
donorFirstNameEntry.pack(fill="x")

# donor last name
frameDonorLastName = tk.Frame(tab2)
donorLastNameLabel = tk.Label(frameDonorLastName, text="donor last name:", width=20)
donorLastNameLabel.pack(side="left")
donorLastNameEntry = tk.Entry(frameDonorLastName)
donorLastNameEntry.pack(fill="x")

# for the type of donor, if he is anonymous
def switchAnonymousDonor():
     if anonymousVar.get() == 1:
          donorFirstNameEntry.config(state="disabled")
          donorLastNameEntry.config(state="disabled")
     else:
          donorFirstNameEntry.config(state="normal")
          donorLastNameEntry.config(state="normal")

frameAnonymous = tk.Frame(tab2)
frameAnonymous.pack(fill="x")
anonymousVar = tk.IntVar()
anonymousCheckBox = tk.Checkbutton(frameAnonymous, text="Anonymous donation ", variable=anonymousVar, onvalue=1, offvalue=0, command=switchAnonymousDonor)
anonymousCheckBox.pack(side="left")

# so that thigs are in the right order
frameDonorFirstName.pack(fill="x")
frameDonorLastName.pack(fill="x")

# this is the text that gives info about the process of the transaction
sideText2 = tk.StringVar()
sideText2.set("")
sideText2Label = tk.Label(tab2, textvariable=sideText2)

# button that submits info from the entry text boxes to the database
def submitInfoDonation():
     if anonymousVar.get() == 0:
          amount = amountEntry.get()
          typeDonation = typeDonationEntry.get()
          donorFirstName = donorFirstNameEntry.get()
          donorLastName = donorLastNameEntry.get()
     
     else:
          amount = amountEntry.get()
          typeDonation = typeDonationEntry.get()
          donorFirstName = "anonymous"
          donorLastName = "anonymous"

     try:
          
          mycursor.execute("INSERT INTO donations (amount, type, donor_id) VALUES ('" + amount + "', '" +
                                                                                     typeDonation + "', " +
                                                                                     " (SELECT id FROM donors WHERE firstname = '" + donorFirstName + "' and " +
                                                                                                                   "lastname = '" + donorLastName + "' ) )")
          amountEntry.delete(0,'end')
          typeDonationEntry.delete(0,'end')
          donorFirstNameEntry.delete(0, 'end')
          donorLastNameEntry.delete(0, 'end')
          
          sideText2.set("data successfully added to the table")

     except Exception as e:
          # ! for debugging purposes
          print(e)
          sideText2.set("error occured")


buttonSubmitDonation = tk.Button(tab2, text="submit info into database", command=submitInfoDonation)

buttonSubmitDonation.pack(fill="x")
sideText2Label.pack()


# * set up of the third tab
titleLabel = tk.Label(tab3, text="retreive data from database", font="bold")
titleLabel.pack()


# opens the root
root.mainloop()
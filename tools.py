from conDB import mydb, mycursor
import tkinter as tk

def createDatabase():
    # creates the database if not existant
    mycursor.execute("CREATE DATABASE IF NOT EXISTS donations_db;")

    # ! whenever you run the program you delete the previous table so that you can play around with the features
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

def addFakeDataDonors():
    mycursor.execute("INSERT IGNORE INTO donors (firstname, lastname, profession, country) VALUES ('John', 'Smith', 'baker', 'Belgium')," +
                                                                                                      "('Elena', 'Jok', 'artist', 'France')," +
                                                                                                      "('Jean', 'Youlk', 'painter', 'Poland');")

def addFakeDataDonations():
    mycursor.execute("INSERT INTO donations (amount, type, donor_id) VALUES (50, 'cash', 1), (45, 'card', 2);")

# * for the second tab, about adding data to the database
def submitInfoDonor(firstnameEntry, lastnameEntry, professionEntry, countryEntry, sideText1):
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

def switchAnonymousDonor(anonymousVar, donorFirstNameEntry, donorLastNameEntry):
     if anonymousVar.get() == 1:
          donorFirstNameEntry.config(state="disabled")
          donorLastNameEntry.config(state="disabled")
     else:
          donorFirstNameEntry.config(state="normal")
          donorLastNameEntry.config(state="normal")

def submitInfoDonation(anonymousVar, amountEntry, typeDonationEntry, donorFirstNameEntry, donorLastNameEntry, sideText2):
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

# this method cleans the output of the databse to a readable table
def prettyRows(rows):
     output = ""
     for row in rows:
          for element in row:
               if type(element) is str:
                    space = "\t\t"
               else:
                    space = "\t"
                    
               output += str(element) + space
          output += "\n"
     return output

def getAllInfoDonors(outputInfo):

    mycursor.execute("SELECT * FROM donors;")
    rows = mycursor.fetchall()

    rows = prettyRows(rows)

    outputInfo.delete("1.0", "end")
    outputInfo.insert(tk.END, rows)

def getAllDonations(outputInfo):
     mycursor.execute("SELECT * FROM donations, donors WHERE donations.donor_id = donors.id;")
     rows = mycursor.fetchall()
     rows = prettyRows(rows)

     outputInfo.delete("1.0", "end")
     outputInfo.insert(tk.END, rows)

def getAllAnonymousDonations(outputInfo):
     mycursor.execute("SELECT * FROM donations WHERE donor_id = (SELECT id FROM donors WHERE firstname = 'anonymous' and lastname = 'anonymous');")
     rows = mycursor.fetchall()
     rows = prettyRows(rows)

     outputInfo.delete("1.0", "end")
     outputInfo.insert(tk.END, rows)

def getLast10Donations(outputInfo):
     mycursor.execute("SELECT * FROM donations, donors WHERE donations.donor_id = donors.id ORDER BY donations.created_at DESC LIMIT 10;")
     rows = mycursor.fetchall()
     rows = prettyRows(rows)

     outputInfo.delete("1.0", "end")
     outputInfo.insert(tk.END, rows)

def searchCustomDonor(firstNameEntry, lastNameEntry, outputInfo):
     firstName = firstNameEntry.get()
     lastName = lastNameEntry.get()

     mycursor.execute("SELECT * FROM donors, donations WHERE donations.donor_id = donors.id and firstname = '" + firstName + "' and lastname = '" + lastName + "';")
     rows = mycursor.fetchall()
     rows = prettyRows(rows)

     outputInfo.delete("1.0", "end")
     outputInfo.insert(tk.END, rows)
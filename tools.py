"""
This is a helper module for the main.py file. It has all the helper methods needed.
"""

if __name__ != "__main__":
     from conDB import mydb, mycursor
     import tkinter as tk


def setUpDatabase():
     """
     This method sets up the database if it does not aleady exists. It creates the database itself,
     it creates the tables, the anonymous entry so that we can add anonymous donations and lastly
     the two triggers related to the donors.
     """

     # creates the database if not existant
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
     
     # this is the anonymous donor for the anonymous donations
     mycursor.execute("INSERT IGNORE INTO donors (firstname, lastname) VALUES ('anonymous', 'anonymous')")

     # the trigger about the number of donations for each user
     mycursor.execute("DROP TRIGGER IF EXISTS number_donation_add")
     mycursor.execute("CREATE TRIGGER number_donation_add AFTER INSERT ON donations " +
                      "FOR EACH ROW " +
                      "BEGIN " +
                         "UPDATE donors " +
                         "SET "+
                              "number_donations = number_donations + 1 " +
                         "WHERE donors.id = NEW.donor_id; " +
                      "END;")

     mycursor.execute("DROP TRIGGER IF EXISTS number_donation_del")
     mycursor.execute("CREATE TRIGGER number_donation_del AFTER DELETE ON donations " +
                      "FOR EACH ROW " +
                      "BEGIN " +
                         "UPDATE donors " +
                         "SET "+
                              "number_donations = number_donations - 1 " +
                         "WHERE donors.id = OLD.donor_id; " +
                      "END;")

     # trigger for counting the toal each donor has donated
     mycursor.execute("DROP TRIGGER IF EXISTS total_donated_add")
     mycursor.execute("CREATE TRIGGER total_donated_add AFTER INSERT ON donations " +
                      "FOR EACH ROW " +
                      "BEGIN " +
                         "UPDATE donors " +
                         "SET "+
                              "total_gifted = total_gifted + NEW.amount " +
                         "WHERE donors.id = NEW.donor_id; " +
                      "END;")

     mycursor.execute("DROP TRIGGER IF EXISTS total_donated_del")
     mycursor.execute("CREATE TRIGGER total_donated_del AFTER DELETE ON donations " +
                      "FOR EACH ROW " +
                      "BEGIN " +
                         "UPDATE donors " +
                         "SET "+
                              "total_gifted = total_gifted - OLD.amount " +
                         "WHERE donors.id = OLD.donor_id; " +
                      "END;")


# * for the second tab, about adding data to the database
def parseInfomationDonor(firstname, lastname, profession, country):

     if not firstname:
          firstname = "NULL"
     else:
          firstname = "'" + firstname + "'"

     if not lastname:
          lastname = "NULL"
     else:
          lastname = "'" + lastname + "'"

     if not profession:
          profession = "'not specified'"
     else:
          profession = "'" + profession + "'"

     if not country:
          country = "'not specified'"
     else:
          country = "'" + country + "'"
     
     return firstname, lastname, profession, country

def submitInfoDonor(firstnameEntry, lastnameEntry, professionEntry, countryEntry, sideText1):
     
     firstname, lastname, profession, country = parseInfomationDonor(firstnameEntry.get(), lastnameEntry.get(), professionEntry.get(), countryEntry.get())

     try:
          mycursor.execute("INSERT INTO donors (firstname, lastname, profession, country) VALUES (" + firstname + ", " +
                                                                                                    lastname + ", " +
                                                                                                    profession + ", " +
                                                                                                    country + ")")
          firstnameEntry.delete(0,'end')
          lastnameEntry.delete(0,'end')
          professionEntry.delete(0, 'end')
          countryEntry.delete(0, 'end')

          sideText1.set("data successfully added to the table")

     except:
          sideText1.set("error occured")

def switchAnonymousDonor(anonymousVar, donorFirstNameEntry, donorLastNameEntry):
     if anonymousVar.get() == 1:
          donorFirstNameEntry.config(state="disabled")
          donorLastNameEntry.config(state="disabled")
     else:
          donorFirstNameEntry.config(state="normal")
          donorLastNameEntry.config(state="normal")

def parseInformationDonation(anonymous, amount, typeDonation, donorFirstName, donorLastName):

     if not amount:
          amount = "NULL"
     
     if not typeDonation:
          typeDonation = "'not specified'"
     else:
          typeDonation = "'" + typeDonation + "'"
     
     if anonymous == 1:
          donorFirstName = "'anonymous'"
          donorLastName = "'anonymous'"
     else:
          donorFirstName = "'" + donorFirstName + "'"
          donorLastName = "'" + donorLastName + "'"

     return amount, typeDonation, donorFirstName, donorLastName

def submitInfoDonation(anonymousVar, amountEntry, typeDonationEntry, donorFirstNameEntry, donorLastNameEntry, sideText2):
     
     amount, typeDonation, donorFirstName, donorLastName = parseInformationDonation(anonymousVar.get(), amountEntry.get(), typeDonationEntry.get(), donorFirstNameEntry.get(), donorLastNameEntry.get())

     try: 
          mycursor.execute("(SELECT id FROM donors WHERE firstname = " + donorFirstName + " and lastname = " + donorLastName + ")")
          donor_id = mycursor.fetchone()[0]
          
          mycursor.execute("INSERT INTO donations (amount, type, donor_id) VALUES (" + amount + ", " +
                                                                                     typeDonation + ", " +
                                                                                     str(donor_id) + " )")

          amountEntry.delete(0,'end')
          typeDonationEntry.delete(0,'end')
          donorFirstNameEntry.delete(0, 'end')
          donorLastNameEntry.delete(0, 'end')

          
          sideText2.set("data successfully added to the table")

     except:
          sideText2.set("error occured")


# * for the third tab
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



# * for the fourth tab
def removeDonor(firstnameEntry, lastnameEntry, sideText1Remove):

     firstname = firstnameEntry.get()
     lastname = lastnameEntry.get()

     if firstname == "anonymous" and lastname == "anonymous":
          sideText1Remove.set("Cannot remove this donor")
          return

     try:
          mycursor.execute("SELECT id FROM donors WHERE firstname = '" + firstname + "' and lastname = '" + lastname + "';")
          donor_id = mycursor.fetchone()
          
          if donor_id is None:
               sideText1Remove.set("could not find donor in database")
               return

          mycursor.execute("UPDATE donations SET donor_id = 1 WHERE donor_id = " + str(donor_id[0]) + ";")

          mycursor.execute("DELETE FROM donors WHERE firstname = '" + firstname + "' and lastname = '" + lastname + "';")

          firstnameEntry.delete(0,'end')
          lastnameEntry.delete(0, 'end')

          sideText1Remove.set("donor successfully removed from database")

     except:
          sideText1Remove.set("error occured")

def switchAnonymousDonorRemove(anonymousVar, donorFirstNameEntry, donorLastNameEntry):
     if anonymousVar.get() == 1:
          donorFirstNameEntry.config(state="disabled")
          donorLastNameEntry.config(state="disabled")
     else:
          donorFirstNameEntry.config(state="normal")
          donorLastNameEntry.config(state="normal")

def removeDonation(anonymousVarRermove, amountEntryRemove, typeDonationEntryRemove, donorFirstNameEntryRemove, donorLastNameEntryRemove, sideText2Remove):
     
     if anonymousVarRermove.get() == 0:
          donorFirstName = donorFirstNameEntryRemove.get()
          donorLastName = donorLastNameEntryRemove.get()
     else:
          donorFirstName = "anonymous"
          donorLastName = "anonymous"
          
     amount = amountEntryRemove.get()
     typeDonation = typeDonationEntryRemove.get()

     try: 
          mycursor.execute("SELECT id FROM donors WHERE firstname = '" + donorFirstName + "' and lastname = '" + donorLastName + "';")
          donor_id = mycursor.fetchone()[0]

          mycursor.execute("DELETE FROM donations WHERE amount = " + amount + " and type = '" + typeDonation + "' and donor_id = " + str(donor_id) + " LIMIT 1;")

          amountEntryRemove.delete(0,'end')
          typeDonationEntryRemove.delete(0,'end')
          donorFirstNameEntryRemove.delete(0, 'end')
          donorLastNameEntryRemove.delete(0, 'end')

          
          sideText2Remove.set("donation successfully removed from database")

     except:
          sideText2Remove.set("could not find donation or donor")

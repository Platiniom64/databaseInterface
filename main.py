import tkinter as tk
from tkinter import ttk

# * set up of the root window
root = tk.Tk()
root.geometry("600x500")
root.title("user interface database")

import conDB
conDB.initialiseConnection()

from tools import *

# this creates the database and the tables
setUpDatabase()


# * creation of the different tabs of the window
rootTab = ttk.Notebook(root)

tab1 = ttk.Frame(rootTab)
rootTab.add(tab1, text="info")

tab2 = ttk.Frame(rootTab)
rootTab.add(tab2, text="add data")

tab3 = ttk.Frame(rootTab)
rootTab.add(tab3, text="retrieve data")

tab4 = ttk.Frame(rootTab)
rootTab.add(tab4, text="remove data")

rootTab.pack(fill="both")

# * set up of the first tab
titleLabel = tk.Label(tab1, text="Information about the program", font="bold")
titleLabel.pack()

frameTextIntro = tk.Frame(tab1)
frameTextIntro.pack(fill="x")
textLabel = tk.Label(frameTextIntro,
                    text="This program was created in order to ease the interaction with the database.\n"+
                         "You can use it in order to add data to the database, retrive data from the database and also to remove\n" +
                         "data is you made a mistake somewhere. Here is an explanation of each tab:\n\n" + 
                         
                         "The tab 'add data' helps you add rows to the database.\n" +
                         "You can enter new donors (as long as they don't exist already) and also new donations.\n" +
                         "Donations can be saved from a donor but can also be anonymous.\n\n" +
                         
                         
                         "The tab 'retrieve data' will help you find data inside the database.\n" +
                         "You have different options to choose from: getting all the donors, getting all the donations,\n" +
                         "getting all the anonymous donations, getting the last 10 donations and lastly finding everything \n" +
                         "connected with a certain donor based on its first name and last name.\n\n" +

                         "The last tab called 'remove data' is to remove rows form the database.\n" +
                         "Again, you can remove donors and donations. If you remove a donor that has made donations, then \n" +
                         "Its donations will become anonymous.\n\n" +

                         "This program works by connecting to a MySQL server. Please install and start a server on your machine.",
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

# this is the text that gives info about the process of the submission to the database
sideText1 = tk.StringVar()
sideText1.set("")
sideText1Label = tk.Label(tab2, textvariable=sideText1)

# button that submits info from the entry text boxes to the database
buttonSubmitDonor = tk.Button(tab2, text="submit info into database", command=lambda:submitInfoDonor(firstnameEntry, lastnameEntry, professionEntry, countryEntry, sideText1))
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
frameAnonymous = tk.Frame(tab2)
frameAnonymous.pack(fill="x")
anonymousVar = tk.IntVar()
anonymousCheckBox = tk.Checkbutton(frameAnonymous, text="Anonymous donation ", variable=anonymousVar, onvalue=1, offvalue=0, command=lambda:switchAnonymousDonor(anonymousVar, donorFirstNameEntry, donorLastNameEntry))
anonymousCheckBox.pack(side="left")

# so that thigs are in the right order
frameDonorFirstName.pack(fill="x")
frameDonorLastName.pack(fill="x")

# this is the text that gives info about the process of the transaction
sideText2 = tk.StringVar()
sideText2.set("")
sideText2Label = tk.Label(tab2, textvariable=sideText2)

# button that submits info from the entry text boxes to the database
buttonSubmitDonation = tk.Button(tab2, text="submit info into database", command=lambda:submitInfoDonation(anonymousVar, amountEntry, typeDonationEntry, donorFirstNameEntry, donorLastNameEntry, sideText2))
buttonSubmitDonation.pack(fill="x")

sideText2Label.pack()


# * set up of the third tab
titleLabel = tk.Label(tab3, text="Retreive data from database", font="bold")
titleLabel.pack()

frameButtons1 = tk.Frame(tab3)
frameButtons1.pack(fill="x")

frameButtons2 = tk.Frame(tab3)
frameButtons2.pack(fill="x")

frameOutputInfo = tk.Frame(tab3)
frameOutputInfo.pack(fill="both")

outputInfo = tk.Text(frameOutputInfo)
outputInfo.pack(fill="both")

getAllInfoDonorButton = tk.Button(frameButtons1, text="get all info from donors", command=lambda:getAllInfoDonors(outputInfo))
getAllInfoDonorButton.pack(side="left")

getAllInfoDonationsButton = tk.Button(frameButtons1, text="get all info about donations", command=lambda:getAllDonations(outputInfo))
getAllInfoDonationsButton.pack(side="left")

getAllAnonymousDonationsButton = tk.Button(frameButtons1, text="get all anonymous donations", command=lambda:getAllAnonymousDonations(outputInfo))
getAllAnonymousDonationsButton.pack(side="left")

getAllAnonymousDonationsButton = tk.Button(frameButtons1, text="get last 10 donations", command=lambda:getLast10Donations(outputInfo))
getAllAnonymousDonationsButton.pack(side="left")

# for finding info about one donor
frameFirstName = tk.Frame(frameButtons2)
frameFirstName.pack(fill="x", side="left")
firstNameLabel = tk.Label(frameFirstName, text="first name donor:", width=15)
firstNameLabel.pack(side="left")
firstNameEntry = tk.Entry(frameFirstName)
firstNameEntry.pack(side="left")

frameLastName = tk.Frame(frameButtons2)
frameLastName.pack(side="left")
lastNameLabel = tk.Label(frameLastName, text="last name donor:", width=15)
lastNameLabel.pack(side="left")
lastNameEntry = tk.Entry(frameLastName)
lastNameEntry.pack(side="left")

searchButton = tk.Button(frameButtons2, text="search", command=lambda:searchCustomDonor(firstNameEntry, lastNameEntry, outputInfo))
searchButton.pack(side="left")

# * set up of the fourth tab

titleLabel = tk.Label(tab4, text="Remove data from the database", font="bold")
titleLabel.pack()

# ----- for removing a donor -----

frameSubtitle1 = tk.Frame(tab4)
frameSubtitle1.pack(fill="x")
subtitle1 = tk.Label(frameSubtitle1, text="Remove a donor here:")
subtitle1.pack(side="left")

# first name
frameFirstname = tk.Frame(tab4)
frameFirstname.pack(fill="x")
firstnameLabel = tk.Label(frameFirstname, text="first name:", width=20)
firstnameLabel.pack(side="left")
firstnameEntryRemove = tk.Entry(frameFirstname)
firstnameEntryRemove.pack(fill="x")

# last name
frameLastname = tk.Frame(tab4)
frameLastname.pack(fill="x")
lastnameLabel = tk.Label(frameLastname, text="last name:", width=20)
lastnameLabel.pack(side="left")
lastnameEntryRemove = tk.Entry(frameLastname)
lastnameEntryRemove.pack(fill="x")

# this is the text that gives info about the process of the submission to the database
sideText1Remove = tk.StringVar()
sideText1Remove.set("")
sideText1RemoveLabel = tk.Label(tab4, textvariable=sideText1Remove)

# button that submits info from the entry text boxes to the database
buttonSubmitDonor = tk.Button(tab4, text="remove from database", command=lambda:removeDonor(firstnameEntryRemove, lastnameEntryRemove, sideText1Remove))
buttonSubmitDonor.pack(fill="x")
sideText1RemoveLabel.pack()


# ----- for removing a donation -----

frameSubtitle2 = tk.Frame(tab4)
frameSubtitle2.pack(fill="x")
subtitle2Label = tk.Label(frameSubtitle2, text="Remove a donation here:")
subtitle2Label.pack(side="left")

# amount of money for donation
frameAmount = tk.Frame(tab4)
frameAmount.pack(fill="x")
amountLabel = tk.Label(frameAmount, text="amount:", width=20)
amountLabel.pack(side="left")
amountEntryRemove = tk.Entry(frameAmount)
amountEntryRemove.pack(fill="x")

# type of donation
frameTypeDonation = tk.Frame(tab4)
frameTypeDonation.pack(fill="x")
typeDonationLabel = tk.Label(frameTypeDonation, text="type of donation:", width=20)
typeDonationLabel.pack(side="left")
typeDonationEntryRemove = tk.Entry(frameTypeDonation)
typeDonationEntryRemove.pack(fill="x")

# donor first name
frameDonorFirstName = tk.Frame(tab4)
donorFirstNameLabel = tk.Label(frameDonorFirstName, text="donor first name:", width=20)
donorFirstNameLabel.pack(side="left")
donorfirstnameEntryRemove = tk.Entry(frameDonorFirstName)
donorfirstnameEntryRemove.pack(fill="x")

# donor last name
frameDonorLastName = tk.Frame(tab4)
donorLastNameLabel = tk.Label(frameDonorLastName, text="donor last name:", width=20)
donorLastNameLabel.pack(side="left")
donorLastNameEntryRemove = tk.Entry(frameDonorLastName)
donorLastNameEntryRemove.pack(fill="x")

# for the type of donor, if he is anonymous
frameAnonymous = tk.Frame(tab4)
frameAnonymous.pack(fill="x")
anonymousVarRermove = tk.IntVar()
anonymousCheckBoxRemove = tk.Checkbutton(frameAnonymous, text="Anonymous donation ", variable=anonymousVarRermove, onvalue=1, offvalue=0, command=lambda:switchAnonymousDonorRemove(anonymousVarRermove, donorfirstnameEntryRemove, donorLastNameEntryRemove))
anonymousCheckBoxRemove.pack(side="left")

# so that things are in the right order
frameDonorFirstName.pack(fill="x")
frameDonorLastName.pack(fill="x")

# this is the text that gives info about the process of the transaction
sideText2Remove = tk.StringVar()
sideText2Remove.set("")
sideText2RemoveLabel = tk.Label(tab4, textvariable=sideText2Remove)

# button that submits info from the entry text boxes to the database
buttonSubmitDonation = tk.Button(tab4, text="remove from database", command=lambda:removeDonation(anonymousVarRermove, amountEntryRemove, typeDonationEntryRemove, donorfirstnameEntryRemove, donorLastNameEntryRemove, sideText2Remove))
buttonSubmitDonation.pack(fill="x")

sideText2RemoveLabel.pack()



# * opens the root
root.mainloop()
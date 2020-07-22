from conDB import mydb, mycursor

def addFakeDataDonors():
    mycursor.execute("INSERT IGNORE INTO donors (firstname, lastname, profession, country) VALUES ('John', 'Smith', 'baker', 'Belgium')," +
                                                                                                      "('Elena', 'Jok', 'artist', 'France')," +
                                                                                                      "('Jean', 'Youlk', 'painter', 'Poland');")
def addFakeDataDonations():
    mycursor.execute("INSERT INTO donations (amount, type, donor_id) VALUES (50, 'cash', 1), (45, 'card', 2);")

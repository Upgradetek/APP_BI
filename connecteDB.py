import mysql.connector


def connecte(Rq):
    myconn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='stage'
    )

    cursor = myconn.cursor()
    cursor.execute(Rq)

    # Fetch all the rows from the result set
    results = cursor.fetchall()
    # formatted_results = [value for row in results for value in row]

    # Close the cursor and connection
    cursor.close()
    myconn.close()
    formatted_results = [value for row in results for value in row]

    return formatted_results


# print(connecte("SELECT  NCompte FROM  compte WHERE Devise = 'EGY'"))
# Retrieve the id from the Country table where the Country is 'france'
# cursor.execute("SELECT id ,idBank ,Agency FROM Agency;")
# Agency = cursor.fetchone()
# cursor.execute("SELECT id ,idCountry,Bank FROM Banks;")
# Banks = cursor.fetchone()
# cursor.execute("SELECT id ,Country FROM Country;")
# Country = cursor.fetchone()
# cursor.execute("SELECT id,idAgency,NCompte,SoldIntial,Devise FROM compte;")
# Compte = cursor.fetchone()
#
# cursor.execute("CREATE TABLE admin_access_requests(id INT AUTO_INCREMENT PRIMARY KEY,firstusername VARCHAR(255) NOT NULL,lastusername VARCHAR(255) NOT NULL,email VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL,request_reason TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending')")

# myconn.commit()  # Commit the changes to the database

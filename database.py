import sqlite3


def oprette_db():
    # Opret forbindelse til databasen
    conn = sqlite3.connect('EKG_data.db')
    # Opret en pegepind, der udfører forespørgslerne
    c = conn.cursor()

    # Opret person-tabel
    c.execute('''CREATE TABLE IF NOT EXISTS person
                 (Person_id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(70), CPR CHAR(11), telefon VARCHAR(20), køn VARCHAR, adresse VARCHAR(100), mail VARCHAR(100))''')

    # Opret målinger-tabel med en fremmed nøgle til person-tabellen
    c.execute('''CREATE TABLE IF NOT EXISTS målinger
                 (Målinger_id INTEGER PRIMARY KEY AUTOINCREMENT, EKG str, Person_id INTEGER, FOREIGN KEY(Person_id) REFERENCES person(Person_id))''')

    conn.commit()
    conn.close()

def add_patient():
    try:
        conn = sqlite3.connect('EKG_data.db')
        c = conn.cursor()
        # Check if a row with the same CPR already exists
        c.execute("SELECT 1 FROM person WHERE CPR = '060666-6666'")
        row1 = c.fetchone()
        c.execute("SELECT 2 FROM person WHERE CPR = '020222-2222'")
        row2 = c.fetchone()

        if row1 is None and row2 is None:
            # Insert new rows
            c.execute("INSERT INTO person(name, CPR, telefon, køn, adresse, mail) VALUES ('John Doe', '060666-6666', '66666666', 'M', 'Humlebien 25, 8100, Vejle', 'sejfyr25@hotmail.com'),('Jane Doe', '020222-2222', '22222222', 'F', 'Carlsberg 7, 2735, Holbæk', 'hejmedddig@hotmail.com')")
            conn.commit()
            print("Rows inserted successfully.")
        else:
            print("A row with the same CPR already exists.")

        c.close()
        conn.close()

    except sqlite3.Error as e:
        print("Communication error:", e)

oprette_db()
add_patient()

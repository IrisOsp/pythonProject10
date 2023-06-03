import sqlite3
from datetime import datetime

def oprette_db():
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS person
                 (name VARCHAR(70), Person_id INTEGER PRIMARY KEY AUTOINCREMENT, CPR CHAR(11), telefon VARCHAR(20), køn VARCHAR, adresse VARCHAR(100), mail VARCHAR(100) )''')
    c.execute('''CREATE TABLE IF NOT EXISTS journal
                 (icd10 VARCHAR(70), Journal_id INTEGER PRIMARY KEY AUTOINCREMENT, anamnese VARCHAR, Person_id INTEGER, FOREIGN KEY(Person_id) REFERENCES person(Person_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS undersøgelse
                 (type VARCHAR(70), Undersøgelse_id INTEGER PRIMARY KEY AUTOINCREMENT, Journal_id INTEGER, FOREIGN KEY(Journal_id) REFERENCES journal(Journal_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS målinger
                 (Sp02 INT, Pulse INT, Målinger_id INTEGER PRIMARY KEY AUTOINCREMENT,created_at DATETIME, Undersøgelse_id INTEGER, FOREIGN KEY(Undersøgelse_id) REFERENCES undersøgelse(Undersøgelse_id))''')

    conn.commit()
    conn.close()

def add_patient():
    try:
        conn = sqlite3.connect('Data.db')
        c = conn.cursor()
        # Check if a row with the same CPR already exists
        c.execute("SELECT 1 FROM person WHERE CPR = '060666-6666'")
        c.execute("SELECT 2 FROM person WHERE CPR = '020222-2222'")
        row = c.fetchone()

        if row is None:
            # Insert a new row
            c.execute("INSERT INTO person(name, CPR, telefon, køn, adresse, mail) VALUES ('John Doe', '060666-6666', '66666666', 'M', 'Humlebien 25, 8100, Vejle', 'sejfyr25@hotmail.com'),('Jane Doe', '020222-2222', '22222222', 'F', 'Carlsberg 7, 2735, Holbæk', 'hejmedddig@hotmail.com')")
            conn.commit()
            print("Row inserted successfully.")
        else:
            print("A row with the same CPR already exists.")

        c.close()
        conn.close()

    except sqlite3.Error as e:
        print("Communication error:", e)

def add_values(s,p):
    try:
        conn=sqlite3.connect('Data.db')
        c=conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO målinger(Sp02,Pulse, created_at) VALUES(?,?,?)",(s,p,created_at));
        conn.commit()
        c.close()
        conn.close()

    except sqlite3.Error as e:
        print("Kommunikationsfejl 3")
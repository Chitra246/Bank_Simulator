import sqlite3

def create_tables():
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    query="""Create Table if not exists accounts(
    AC_No Integer primary key autoincrement,
    Name text,
    Password Text,
    Balance Float,
    Mob_No Text,
    Aadhar Text,
    Email text,
    opendate datetime
    )
    """
    curobj.execute(query)
    conobj.close()
    print("table created or exists")
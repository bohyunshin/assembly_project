import sqlite3

conn = sqlite3.connect("assembly.db", isolation_level=None)

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS assembly 
          (billNum integer PRIMARY KEY, 
           billName text,
           billId text,
           proposerCategory text,
           proposerData text,
           decisionDate text,
           decisionResult text,
           mainProposer text,
           subProposer text)""")

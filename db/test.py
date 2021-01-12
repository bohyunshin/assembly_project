import sqlite3

def updateOneRow(db, vals_list):
    db_conn = sqlite3.connect(db, isolation_level=None)
    c = db_conn.cursor()

    c.execute("""
                INSERT INTO 
                assembly(
                billNum, 
                billName,
                billId,
                proposerCategory,
                proposerData,
                decisionDate,
                decisionResult,
                mainProposer,
                subProposer) 
                VALUES(?,?,?,?,?,?,?,?,?)
                """, vals_list)

vals_list = [1,'a','b','c','d','e','f','g','e']
updateOneRow('assembly.db', vals_list)
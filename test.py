import sqlite3 as sql
con=sql.connect('database.db')
cur=con.cursor()
cur.execute("select * from disease where p_id=(?)",(100,))
print(cur.fetchall())
cur.execute
import sqlite3
con = sqlite3.connect('expense.db')
cur = con.cursor();
cur.execute('select * from expense;')
row=cur.fetchone()
print(row)
row=cur.fetchone()
print(row)
con.commit()
cur.close()
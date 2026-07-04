import sqlite3
con = sqlite3.connect('test.db')
curr = con.cursor();
curr.execute('insert into expenses values (1,250, "food", "04-07-2026");')
curr.execute('insert into expenses values (2,1200,"rent","05-07-2026");')
con.commit()
curr.execute('select * from expenses')
row=curr.fetchone()
print(row);
row=curr.fetchone()
print(row);
curr.close()
con.close()
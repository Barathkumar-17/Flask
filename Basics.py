from flask import Flask, jsonify,request
import sqlite3
con=sqlite3.connect('test.db',check_same_thread=False)
curr=con.cursor()

app = Flask(__name__)

@app.route('/')
def home():
    return "Expense Tracker API is running!"

@app.route('/expenses')
def get_expenses():
    curr.execute('select * from expenses;')
    rows=curr.fetchall()
    return jsonify(rows)

@app.route('/expenses/<int:expense_id>')
def get_expense(expense_id):
    curr.execute('select * from expenses where id = ?;',(expense_id,))
    row=curr.fetchone()
    if(row):
        return jsonify(f"id : {row[0]}, amount : {row[1]} , category : {row[2]}, date : {row[3]}")
    return jsonify({"error": "Expense not found"}), 404

@app.route('/expenses',methods=['POST'])
def add_expense():
    data=request.get_json();
    curr.execute("insert into expenses values ((SELECT IFNULL(MAX(id), 0) + 1 FROM expenses),?,?,?);",
                    (data["amount"],data["category"],data["date"],))
    #note there is no '?' rather just ? as it acts a simple placeholder instead of formatting the string into the string
    # the select iF null finds last id and then +1 .... 
    con.commit()
    curr.execute("select * from expenses where id= last_insert_rowid();")
    expense=curr.fetchone()
    return jsonify(expense),201;

@app.route('/expenses/<int:expense_id>',methods=['PUT'])
def update_expense(expense_id):
    data=request.get_json()
    curr.execute("""update expenses set amount=?,category=?,date=?where id=?;""",
                     (data["amount"],data["category"],data["date"],expense_id))
    con.commit()
    if(curr.rowcount==1):
            curr.execute('select * from expenses where id = ?;',(expense_id,))
            row=curr.fetchone()
            return jsonify(f"id : {row[0]}, amount : {row[1]} , category : {row[2]}, date : {row[3]}"),200
    return jsonify({"error": "Expense not found"}),404

@app.route('/expenses/<int:expense_id>',methods=['DELETE'])
def delete_expense(expense_id):
    curr.execute('delete from expenses where id =?;',(expense_id,))
    con.commit()
    if(curr.rowcount!=0):
            return jsonify({"Deleted" : f"Removed expense with id {expense_id}"}) ,200
    return jsonify({"Error" :  "not found"}),404

if __name__ == '__main__':
    app.run(debug=True)
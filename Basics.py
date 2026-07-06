from flask import Flask, jsonify,request
import sqlite3
con=sqlite3.connect('test.db',check_same_thread=False)
curr=con.cursor()

app = Flask(__name__)
app.json.sort_keys = False
#for making JSON print as required order

@app.route('/')
def home():
    return "Expense Tracker API is running!"

@app.route('/expenses')
def get_expenses():
    curr.execute('select * from expenses;')
    rows=curr.fetchall()
    l=[]
    for i in rows:
        l.append({"id":i[0],"amount": i[1],"category":i[2],"date":i[3]})
    return jsonify(l)

@app.route('/expenses/<int:expense_id>')
def get_expense(expense_id):
    curr.execute('select * from expenses where id = ?;',(expense_id,))
    row=curr.fetchone()
    if(row):
        return jsonify({"id":row[0],"amount": row[1],"category":row[2],"date":row[3]})
    return jsonify({"error": "Expense not found"}), 404

def validate_json(data):
    if not data:
        return jsonify({"Error":"Body not found"}),400
    if "amount" not in data : 
        return jsonify({"Error":"Amount not found"}) , 400
    elif type(data["amount"]) not in (float,int):
        return jsonify({"Error":"Invalid Amount"}),400
    if "category" not in data:
        return jsonify({"Error" : "Category not found"}),400
    elif type(data["category"])!=str:
        return jsonify({"Error":"Invalid Category"}),400
    if "date" not in data:
        return jsonify({"Error" : "Date not found"}),400
    elif type(data["date"])!=str:
        return jsonify({"Error":"Invalid Date"}),400
    return None;

@app.route('/expenses',methods=['POST'])
def add_expense():
    data=request.get_json();
    error = validate_json(data);
    if error:
        return error;
    curr.execute("insert into expenses values ((SELECT IFNULL(MAX(id), 0) + 1 FROM expenses),?,?,?);",
                    (data["amount"],data["category"],data["date"],))
    #note there is no '?' rather just ? as it acts a simple placeholder instead of formatting the string into the string
    # the select iF null finds last id and then +1 .... 
    con.commit()
    curr.execute("select * from expenses where id= last_insert_rowid();")
    row=curr.fetchone()
    return jsonify({"id":row[0],"amount": row[1],"category":row[2],"date":row[3]}),201;

@app.route('/expenses/<int:expense_id>',methods=['PUT'])
def update_expense(expense_id):
    data=request.get_json()
    curr.execute("""update expenses set amount=?,category=?,date=?where id=?;""",
                     (data["amount"],data["category"],data["date"],expense_id))
    con.commit()
    if(curr.rowcount==1):
            curr.execute('select * from expenses where id = ?;',(expense_id,))
            row=curr.fetchone()
            return jsonify({"id":row[0],"amount": row[1],"category":row[2],"date":row[3]}),200
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
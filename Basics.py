from flask import Flask, jsonify,request

app = Flask(__name__)

@app.route('/')
def home():
    return "Expense Tracker API is running!"

expenses = [
    {"id": 1, "amount": 250, "category": "food", "date": "2026-06-28"},
    {"id": 2, "amount": 1200, "category": "rent", "date": "2026-06-01"}
]

@app.route('/expenses')
def get_expenses():
    return jsonify(expenses)

@app.route('/expenses/<int:expense_id>')
def get_expense(expense_id):
    for i in range(0, len(expenses)):
        if expenses[i]['id'] == expense_id:
            return jsonify(expenses[i])
    return jsonify({"error": "Expense not found"}), 404

@app.route('/expenses',methods=['POST'])
def add_expense():
    data=request.get_json();
    expense={
        "id":3,"amount":data['amount'],"category":data['category'] ,"date":data['date'] }
    expenses.append(expense);
    return jsonify(expense),201;
if __name__ == '__main__':
    app.run(debug=True)
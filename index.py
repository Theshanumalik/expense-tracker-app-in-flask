from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/expense_track'
db = SQLAlchemy(app)

class Expense_data(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.String(120), nullable=False)

@app.route('/', methods=['POST', 'GET'])
def home():
    if (request.method == 'POST'):
        title = request.form.get("title")
        amount = request.form.get("amount")
        date = request.form.get("datetime")
        entry = Expense_data(title = title, amount = amount, timestamp = date)
        db.session.add(entry)
        db.session.commit()
        data = Expense_data.query.order_by(Expense_data.sno.desc()).all()
        total_amount = 0
        for expense in data:
            total_amount = total_amount + int(expense.amount)
        return render_template("index.html", data=data, total_amount=total_amount)


    elif(request.method == "GET"):
        data = Expense_data.query.order_by(Expense_data.sno.desc()).all()
        total_amount = 0
        for expense in data:
            total_amount = total_amount + int(expense.amount)
        return render_template("index.html", data=data, total_amount=total_amount)

if(__name__ == "__main__"):
    app.run(debug=True , port= 5000)
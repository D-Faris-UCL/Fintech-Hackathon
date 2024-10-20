from flask import Flask, render_template, request, session, redirect, jsonify
from cs50 import SQL
from currentStock import get_current_stock_price, get_current_stock_name, get_current_stock_esg
import script  # Import your script

app = Flask(__name__)
db = SQL("sqlite:///fintech.db")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        name = get_current_stock_name(symbol)
        print(name)
        price = round(float(get_current_stock_price(symbol)),3)
        amount = float(request.form.get("amount"))
        value = round(price * amount, 3)
        esg = float(get_current_stock_esg(symbol, "static/combined_data.json"))
        stocks = db.execute("SELECT * FROM portfolio")
        for stock in stocks:
            if stock["symbol"] == symbol:
                db.execute("UPDATE portfolio SET amount = ? WHERE symbol = ?", stock["amount"] + amount, symbol)
                db.execute("UPDATE portfolio SET value = ? WHERE symbol = ?", stock["value"] + value, symbol)
                return redirect("/")
        db.execute("INSERT INTO portfolio (symbol, name, price, amount, value, esg) VALUES (?, ?, ?, ?, ?, ?)", symbol, name, price, amount, value, esg)
        return redirect("/")

    stocks = db.execute("SELECT * FROM portfolio")
    my_esg = 0
    for stock in stocks:
        my_esg += stock["esg"] * stock["value"]
    try:
        my_esg /= sum([stock["value"] for stock in stocks])
    except ZeroDivisionError:
        my_esg = 0
    my_esg = round(my_esg, 2)
    return render_template("index.html", stocks=stocks, my_esg = my_esg)

@app.route('/remove', methods=['POST'])
def remove():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        print(symbol)
        db.execute("DELETE FROM portfolio WHERE symbol = ?", symbol)
        return redirect("/")

@app.route("/api/data", methods=["GET"])
def get_data():
    package = {}
    stocks = db.execute("SELECT * FROM portfolio")
    for stock in stocks:
        price = round(float(get_current_stock_price(stock["symbol"])),3)
        value = round(price * stock["amount"], 3)
        package[stock["symbol"]] = {"price": price, "value": value}
    print(package)
    return jsonify(package)

@app.route("/recommendation", methods=["GET"])
def recommendation():
    return render_template("recommendation.html")



if __name__ == '__main__':
    app.run(debug=True,port=5001)
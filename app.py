from flask import Flask, render_template, request, session, redirect, jsonify
from cs50 import SQL
from currentStock import get_current_stock_price, get_current_stock_name, get_current_stock_esg
from datetime import datetime, timedelta
import json

app = Flask(__name__)
db = SQL("sqlite:///fintech.db")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        name = get_current_stock_name(symbol)
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
    print(stocks)
    my_esg = 0
    portfolio_value = 0
    for stock in stocks:
        my_esg += stock["esg"] * stock["value"]
    try:
        my_esg /= sum([stock["value"] for stock in stocks])
        portfolio_value = sum([stock["value"] for stock in stocks])
    except ZeroDivisionError:
        my_esg = 0
    my_esg = round(my_esg, 2)
    portfolio_value = round(portfolio_value, 2)
    return render_template("index.html", stocks=stocks, my_esg = my_esg, portfolio_value = portfolio_value)

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

@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():

    recommendations = [ {"symbol":"AAPL"}, {"symbol":"MSFT"}]

    if request.method == "POST":
        portfolio = []
        sustainability = float(request.form.get("sustainability"))/100
        returns = float(request.form.get("returns"))/100
        risk = float(request.form.get("risk"))/100
        week = int(request.form.get("week"))
        current_date = datetime.now().date()
        new_date = current_date + timedelta(weeks=week)
        stocks = db.execute("SELECT * FROM portfolio")
        for stock in stocks:
            portfolio.append((stock["symbol"], stock["amount"] * float(get_current_stock_price(stock["symbol"]))))
        

        '''
        # Step 1: Open the JSON file
        with open('data.json', 'r') as file:
            # Step 2: Load the JSON data into a dictionary
            data = json.load(file)

        symbol = data["symbol"]
        name = get_current_stock_name(data["symbol"])
        price = round(float(get_current_stock_price(data["symbol"])),3)
        amount = float(request.form.get("amount"))
        value = round(price * amount, 3)
        esg = float(get_current_stock_esg(data["symbol"], "static/combined_data.json"))
        

        # Now you can use the `data` dictionary
        '''


        for recommendation in recommendations:
            recommendation["image"] = f"plots/{recommendation['symbol']}_historical_and_predicted_prices.jpg"

    print(recommendations)
    return render_template("recommendation.html", recommendations = recommendations)


#(symbol,value)
# targetstock 




if __name__ == '__main__':
    app.run(debug=True,port=5001)
import yfinance as yf

def get_current_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        current_price = stock.fast_info["last_price"]
        print(f"The current price of {symbol.upper()} is {current_price}")
        return current_price
    except KeyError:
        print(f"Symbol '{symbol}' not found. Please check the stock symbol and try again.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


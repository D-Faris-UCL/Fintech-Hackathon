import yfinance as yf
import json

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

def get_current_stock_name(symbol):
    try:
        stock = yf.Ticker(symbol)
        name = stock.info["longName"]
        print(f"The current price of {symbol.upper()} is {name}")
        return name
    except KeyError:
        print(f"Symbol '{symbol}' not found. Please check the stock symbol and try again.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_current_stock_esg(symbol, filename):
    try:
        # Load the data from the JSON file
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Ensure the symbol is uppercase
        symbol = symbol.upper()
        
        # Check if the symbol exists in the data
        if symbol in data:
            company_data = data[symbol]
            return(company_data.get('esg_score'))
        else:
            print(f"No data found for {symbol}.")
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON data.")



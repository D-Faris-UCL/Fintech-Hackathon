import yfinance as yf
import json
import csv

# Function to parse the nasdaqlisted.txt and extract the stock symbols
def parse_nasdaq_listed(filename):
    symbols = []
    
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='|')  # Pipe-delimited file
        
        # Skip the header row
        next(reader)
        
        # Process each row
        for row in reader:
            # Stop when reaching the footer (which starts with "File Creation Time")
            if 'File Creation Time' in row[0]:  
                break
            
            # The first column contains the stock symbol
            symbol = row[0]
            if symbol:  # Ensure it's not empty
                symbols.append(symbol)
    
    return symbols

# Example usage
filename = 'nasdaqlisted.txt'  # Replace with the path to your nasdaqlisted.txt file
nasdaq_symbols = parse_nasdaq_listed(filename)

# Print the first few symbols to verify
print(nasdaq_symbols[:10])  # Print first 10 symbols

# Optionally, you can save the symbols to a file or use them in further processing

# Function to fetch historical data for a stock symbol
import yfinance as yf
import json

# Function to fetch weekly historical data for a stock symbol
def fetch_historical_data(symbol, period='1y', interval='1wk'):
    stock_data = yf.download(symbol, period=period, interval=interval)
    
    if not stock_data.empty:
        print(f"Weekly historical data fetched for {symbol}")
        return stock_data
    else:
        print(f"No historical data available for {symbol}")
        return None

# Function to combine market data for multiple symbols
def combine_data(symbols):
    combined_data = {}
    for symbol in symbols:
        print(f"Processing {symbol}...")
        historical_data = fetch_historical_data(symbol)
        
        if historical_data is not None:
            # Reset index to make 'Date' a column and convert it to string
            historical_data = historical_data.reset_index()
            historical_data['Date'] = historical_data['Date'].astype(str)  # Convert Timestamp to string
            
            combined_data[symbol] = historical_data.to_dict(orient='records')
        else:
            print(f"No data available for {symbol}")
    
    return combined_data

# Save combined data to JSON
def save_to_json(data, filename):
    if data:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

# Main script
if __name__ == "__main__":
    # Example stock symbols (you can add more)

    # Step 1: Combine data for the given symbols
    combined_data = combine_data(nasdaq_symbols)

    # Step 2: Save to JSON file
    save_to_json(combined_data, 'yfinance_weekly_stock_data.json')

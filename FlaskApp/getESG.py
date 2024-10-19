import json

# Function to load data and retrieve ESG score and weekly closing prices for a specific company symbol
def get_esg_and_closing_data(symbol, filename):
    try:
        # Load the data from the JSON file
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Ensure the symbol is uppercase
        symbol = symbol.upper()
        
        # Check if the symbol exists in the data
        if symbol in data:
            company_data = data[symbol]
            # Display ESG score
            print(f"ESG Score for {symbol}: {company_data.get('esg_score', 'N/A')}")
            return(company_data.get('esg_score'))
        else:
            print(f"No data found for {symbol}.")
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON data.")

# Main script
if __name__ == "__main__":
    # Replace 'esg_closing_data.json' with the actual path to your JSON file
    data_filename = 'combined_data.json'

    # Get the company symbol from the user
    company_symbol = input("Enter the company symbol to get ESG data and closing prices: ").upper()

    # Call the function to get ESG score and closing prices
    get_esg_and_closing_data(company_symbol, data_filename)

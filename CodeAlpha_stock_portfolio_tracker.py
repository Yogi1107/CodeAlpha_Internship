import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

class StockPortfolio:
    def __init__(self):
        # Initialize an empty DataFrame to hold portfolio data
        self.portfolio = pd.DataFrame(columns=['Stock', 'Quantity', 'Purchase Price'])

    def add_stock(self, stock_symbol, quantity, purchase_price):
        # Check if the stock already exists in the portfolio
        if stock_symbol in self.portfolio['Stock'].values:
            # Update quantity if stock already exists
            self.portfolio.loc[self.portfolio['Stock'] == stock_symbol, 'Quantity'] += quantity
        else:
            # Create a new DataFrame for the new stock entry
            new_stock = pd.DataFrame({'Stock': [stock_symbol], 'Quantity': [quantity], 'Purchase Price': [purchase_price]})
            # Concatenate the new stock entry with the existing portfolio DataFrame
            self.portfolio = pd.concat([self.portfolio, new_stock], ignore_index=True)

    def remove_stock(self, stock_symbol, quantity):
        if stock_symbol in self.portfolio['Stock'].values:
            # Get the current quantity of the stock in the portfolio
            current_quantity = self.portfolio.loc[self.portfolio['Stock'] == stock_symbol, 'Quantity'].values[0]
            if current_quantity >= quantity:
                # Remove the specified quantity from the portfolio
                self.portfolio.loc[self.portfolio['Stock'] == stock_symbol, 'Quantity'] -= quantity
                if self.portfolio.loc[self.portfolio['Stock'] == stock_symbol, 'Quantity'].values[0] == 0:
                    # Remove the stock from the portfolio if the quantity is 0
                    self.portfolio = self.portfolio[self.portfolio['Stock'] != stock_symbol]
            else:
                return f"Not enough stock to remove. Available: {current_quantity}"
        else:
            return "Stock not found in portfolio."

    def track_performance(self):
        portfolio_value = 0
        performance_details = []
        # Iterate through the portfolio to get the stock data
        for row in self.portfolio.iterrows():
            stock_symbol = row['Stock']
            try:
                # Get the latest stock data using Yahoo Finance
                stock_data = yf.Ticker(stock_symbol).history(period='1d')
                if stock_data.empty:
                    raise ValueError(f"No data available for {stock_symbol}")
                
                current_price = stock_data['Close'].iloc[-1]
                value = current_price * row['Quantity']
                portfolio_value += value
                performance_details.append(f"{stock_symbol}: {row['Quantity']} shares, Purchase Price: ${row['Purchase Price']}, Current Price: ${current_price}, Value: ${value}")
            except Exception as e:
                performance_details.append(f"{stock_symbol}: Error - {str(e)}")

        performance_details.append(f"\nTotal Portfolio Value: ${portfolio_value}")
        return performance_details

    def plot_performance(self):
        stock_prices = []
        stock_symbols = self.portfolio['Stock'].values

        # Retrieve the latest prices for each stock
        for stock_symbol in stock_symbols:
            try:
                stock_data = yf.Ticker(stock_symbol).history(period='1y')
                if stock_data.empty:
                    raise ValueError(f"No data available for {stock_symbol}")
                stock_prices.append(stock_data['Close'].iloc[-1])
            except Exception as e:
                stock_prices.append(None)  # Append None for missing data
                print(f"Error retrieving data for {stock_symbol}: {str(e)}")

        # Filter out None values (stocks without data)
        valid_data = [(symbol, price) for symbol, price in zip(stock_symbols, stock_prices) if price is not None]
        
        if valid_data:
            valid_symbols, valid_prices = zip(*valid_data)
            df = pd.DataFrame({
                'Stock': valid_symbols,
                'Last Price': valid_prices
            })
            df.set_index('Stock', inplace=True)
            # Plot the stock prices
            df.plot(kind='bar', figsize=(10, 5))
            plt.title("Stock Performance")
            plt.ylabel("Price in USD")
            plt.show()
        else:
            print("No valid data available for plotting.")

class StockPortfolioGUI:
    def __init__(self, root, portfolio):
        self.root = root
        self.portfolio = portfolio
        self.root.title("Stock Portfolio Tracker")

        # Add stock input fields
        self.stock_symbol_label = tk.Label(root, text="Stock Symbol:")
        self.stock_symbol_label.grid(row=0, column=0)

        self.stock_symbol_entry = tk.Entry(root)
        self.stock_symbol_entry.grid(row=0, column=1)

        self.quantity_label = tk.Label(root, text="Quantity:")
        self.quantity_label.grid(row=1, column=0)

        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=1, column=1)

        self.purchase_price_label = tk.Label(root, text="Purchase Price:")
        self.purchase_price_label.grid(row=2, column=0)

        self.purchase_price_entry = tk.Entry(root)
        self.purchase_price_entry.grid(row=2, column=1)

        # Add buttons for stock operations
        self.add_button = tk.Button(root, text="Add Stock", command=self.add_stock)
        self.add_button.grid(row=3, column=0)

        self.remove_button = tk.Button(root, text="Remove Stock", command=self.remove_stock)
        self.remove_button.grid(row=3, column=1)

        # Track portfolio performance button
        self.track_button = tk.Button(root, text="Track Portfolio Performance", command=self.track_performance)
        self.track_button.grid(row=4, column=0)

        # Plot portfolio performance button
        self.plot_button = tk.Button(root, text="Plot Portfolio Performance", command=self.plot_performance)
        self.plot_button.grid(row=4, column=1)

        # Text box for displaying portfolio performance
        self.performance_text = tk.Text(root, height=10, width=50)
        self.performance_text.grid(row=5, column=0, columnspan=2)

    def add_stock(self):
        stock_symbol = self.stock_symbol_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
            purchase_price = float(self.purchase_price_entry.get())
            self.portfolio.add_stock(stock_symbol, quantity, purchase_price)
            messagebox.showinfo("Success", f"Added {quantity} shares of {stock_symbol} at ${purchase_price} each.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for quantity and price.")

    def remove_stock(self):
        stock_symbol = self.stock_symbol_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
            result = self.portfolio.remove_stock(stock_symbol, quantity)
            if result:
                messagebox.showinfo("Success", f"Removed {quantity} shares of {stock_symbol}.")
            else:
                messagebox.showerror("Error", result)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid quantity.")

    def track_performance(self):
        performance_details = self.portfolio.track_performance()
        self.performance_text.delete(1.0, tk.END)  # Clear previous content
        for detail in performance_details:
            self.performance_text.insert(tk.END, detail + "\n")

    def plot_performance(self):
        self.portfolio.plot_performance()

# Main function to run the GUI
def main():
    portfolio = StockPortfolio()
    root = tk.Tk()
    gui = StockPortfolioGUI(root, portfolio)
    root.mainloop()

if __name__ == "__main__":
    main()

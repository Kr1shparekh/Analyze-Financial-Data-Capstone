#import libraries 
import yfinance as yf 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np

#set stock tickers and date range 
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
start_date = '2020-01-01'
end_date = '2025-01-01'

# Download closing prices for the tickers
data = yf.download(tickers, start=start_date, end=end_date)['Close']

# Fix 1: Proper NaN handling
data = data.dropna()  # Remove inplace=True and reassign

# Fix 2: Correct plotting logic
plt.figure(figsize=(14, 6))

# Plot each stock's time series
for ticker in tickers:
    plt.plot(data.index, data[ticker], label=ticker)  # Add index and data[ticker]

plt.title('Stock Closing Prices (2020-2025)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


#calculating daily returns 

daily_returns = data.pct_change().dropna()
print("\nDaily Returns Summary:")
print(daily_returns.describe())

#plotting daily returns 
plt.figure(figsize=(14, 6))
sns.lineplot(data=daily_returns)
plt.title("Daily Returns of Stocks (2020-2025)")
plt.xlabel("Date")
plt.ylabel("Daily Return")
plt.grid(True)
plt.tight_layout()
plt.show()

#Annualized Returns and Volatility 

avg_annual_return = daily_returns.mean() * 252 # 252 trading days in a year
annual_volatility = daily_returns.std() * (252 ** 0.5)  # Annualized volatility

#combining tthhe results into a data frame 

summary_stats = pd.DataFrame({'Annualized Return (%)': avg_annual_return * 100, 
                              'Annualized Volatility(%)': annual_volatility * 100})

print("\nAnnualized Returns and Volatility:")
print(summary_stats.round(2))


#correlation matrix pofd daily returns 

correlation_matrix = daily_returns.corr()
#plotting heatmap 
plt.figure(figsize=(10,6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Correlation Matrix of Daily Returns")
plt.tight_layout()
plt.show()


#set random seed for reproducibility
np.random.seed(42)

# Number of portfolios to simulate
num_portfolios = 10000

#store results in lists 

results = {
    'Return' : [],
    'Volatility': [],
    'Sharpe Ratio': [],
    'Weights': []
}

for _ in range(num_portfolios):
    # Generate random weights
    weights = np.random.random(len(tickers))
    weights /= np.sum(weights)  # Normalize to sum to 1

    # Calculate portfolio return and volatility
    portfolio_return = np.sum(weights * avg_annual_return)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(daily_returns.cov() * 252, weights)))

    # Calculate Sharpe Ratio (assuming risk-free rate is 0)
    sharpe_ratio = portfolio_return / portfolio_volatility

    # Store results
    results['Return'].append(portfolio_return)
    results['Volatility'].append(portfolio_volatility)
    results['Sharpe Ratio'].append(sharpe_ratio)
    results['Weights'].append(weights)

# Convert results to DataFrame
portfolios = pd.DataFrame(results)

plt.figure(figsize=(12, 6))
scatter = plt.scatter(
    portfolios['Volatility'], 
    portfolios['Return'], 
    c=portfolios['Sharpe Ratio'], 
    cmap='viridis', 
    alpha=0.7
)
plt.colorbar(scatter, label='Sharpe Ratio')
plt.xlabel('Volatility (Risk)')
plt.ylabel('Expected Return')
plt.title('Efficient Frontier of Simulated Portfolios')
plt.grid(True)
plt.tight_layout()
plt.show()


#finding portfolio with max sharpe ratio 
max_sharpe = portfolios.iloc[portfolios['Sharpe Ratio'].idxmax()]

#finding portfolio with minimum sharpe rario 
min_sharpe = portfolios.iloc[portfolios['Sharpe Ratio'].idxmin()]

#balanced portfolio 

# Balanced portfolio: closest to average Sharpe Ratio
balanced = portfolios.iloc[(portfolios['Sharpe Ratio'] - portfolios['Sharpe Ratio'].mean()).abs().idxmin()]


#displaying alllocations 

def print_portfolios(name, portfolio): 
    print(f"n\n{name} Portfolio:")
    for i, weight in enumerate(portfolio['Weights']):
        print(f"{tickers[i]}: {round(weight*100,2)}%")
        print(f"Expected Return: {round(portfolio['Return']*100,2)}%")
        print(f"Volatility: {round(portfolio['Volatility']*100,2)}%")
        print(f"Sharpe Ratio: {round(portfolio['Sharpe Ratio'],2)}")

        print_portfolio("Conservative", min_sharpe)
        print_portfolio("Aggressive", max_sharpe)
        print_portfolio("Balanced", balanced)

def plot_weights(portfolio, title):
    weights = portfolio['Weights']
    plt.figure(figsize=(8, 5))
    plt.bar(tickers, weights, color='skyblue')
    plt.title(f"{title} Portfolio Allocation")
    plt.ylabel("Weight")
    plt.xlabel("Ticker")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


plot_weights(min_sharpe, "Conservative")
plot_weights(balanced, "Balanced")
plot_weights(max_sharpe, "Aggressive")

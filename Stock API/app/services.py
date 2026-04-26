import yfinance  as yf
from flask import current_app
import requests
import pandas as pd

# Use a persistent session with real-world headers
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
})

# Function to fetch Comapny Details
def get_company_data(symbol: str):

    try:
        ticker = yf.Ticker(symbol)
        
        # Try fetching history first; it's more reliable for 'waking up' the API
        hist = ticker.history(period="1d")
        if hist.empty:
            print(f"History is empty for {symbol} ---")
            
        info = ticker.info

        if not info or 'longName' not in info:
            return None


        return {
            "symbol": symbol.upper(),
            "company_name": info.get("longName"),
            "business_summary": info.get("longBusinessSummary"),
            "industry": info.get("industry"),
            "sector": info.get("sector"),
            "key_officers": [
                {"name": officer.get("name"), "title": officer.get("title")}
                for officer in info.get("companyOfficers", [])
            ]
        }
    except Exception as e:
        print(f"ERROR: {str(e)} ---")
        return None
    
# Function to get latest price, change and other info of stock in market in relatime

def get_market_data(symbol:str):

    try:
        ticker = yf.Ticker(symbol)

        fast = ticker.fast_info

        current_price = fast.last_price
        prev_close = fast.previous_close
        price_change = current_price - prev_close
        pct_change = ((price_change / prev_close) * 100)

        return {
            'symbol':symbol.upper(),
            "current_price": round(current_price, 2),
            "Prevoius close": round(prev_close, 2),
            "Price change": round(price_change, 2),
            "Percentage change": round(pct_change, 2),
            "Day_high": fast.day_high,
            "Day_low": fast.day_low,
            "exchange": fast.exchange,
            "currency": fast.currency
        }
    except Exception as e:
        print(f"Error -- str{e}  -----")
        return None
    

# Function to get hidtorical data of comapny

def get_historical_data(symbol, start_date, end_date, interval='1d'):
    
    try:
        ticker = yf.Ticker(symbol)

        df = ticker.history(start=start_date, end=end_date, interval=interval)

        if df.empty:
            return None
        
        # Reset index to move the Date from the index to a column
        df = df.reset_index()

        # Convert Date to string for JSON serialization
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

        # Convert the DataFrame to a list of dictionaries
        return df.to_dict(orient='records')
    except Exception as e:
        print(f'Historical Date Error : {e}')
        return None
    
def analyse_stock_data(df):
    """Performs Techincal analysis on dataframe histroical data"""

    if df.empty:
        return None
    
    # calculate simple moving averages (SMA)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()

    # calculate daily returns & volatility
    df['Daily_Return'] = df['Close'].pct_change()
    volatility = df['Daily_Return'].std() * (252**0.5)

    # Generate Actionable Signal (Example: SMA Crossover)
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    trend = "Netural"
    if latest['SMA_20'] > latest['SMA_50']:
        trend = "Bullish"
    elif latest['SMA_20'] > latest['SMA_50']:
        trend = "Bearish"

    # Price performance
    total_return = ((latest['Close'] - df.iloc[0]['Close']) / df.iloc[0]['Close']) * 100

    return {
        "summary": {
            "latest_close": round(latest['Close'], 2),
            "period_return_pct": f"{total_return:.2f}%",
            "annualized_volatility": f"{volatility:.2f}%",
            "trend_analysis": trend
        },
        "indicators": {
            "sma_20": round(latest['SMA_20'], 2) if not pd.isna(latest['SMA_20']) else None,
            "sma_50": round(latest['SMA_50'], 2) if not pd.isna(latest['SMA_50']) else None
        },
        "action_item": "Strong Buy" if total_return > 5 and trend.startswith("Bullish") else "Monitor"
    }
    






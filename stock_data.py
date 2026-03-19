import yfinance as yf

def get_real_time_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            return None

        price = data["Close"].iloc[-1]

        return round(float(price), 2)

    except Exception as e:
        print("Stock API error:", e)
        return None
import yfinance as yf
import asyncio
import os
import csv
import pandas as pd
import datetime


def get_historical_data(ticker, start_date=None, end_date=None, time_frame=None):
    if start_date and end_date:
        stock = yf.Ticker(ticker)
        historical_data = stock.history(start=start_date, end=end_date)
        historical_data = clean_data(historical_data)
        return historical_data
    elif time_frame:
        stock = yf.Ticker(ticker)
        historical_data = stock.history(period=time_frame)
        historical_data = clean_data(historical_data)
        return historical_data
    else:
        raise ValueError("Invalid arguments, provide either start_date and end_date or time_frame")


def save_data_to_csv(dataframe, filename):
    dataframe.to_csv(os.path.join(os.getcwd(), "data/historical_price_data", filename), index=False)


async def update_historical_data():
    print("Updating Data")
    while True:
        current_time = datetime.datetime.now().time()
        if datetime.time(0, 0) < current_time < datetime.time(0, 1):
            for file in os.listdir(os.path.join(os.getcwd(), "data/historical_price_data")):
                if file.endswith(".csv"):
                    ticker = file.split(".")[0]
                    stock = yf.Ticker(ticker)
                    historical_data = stock.history(interval='max')
                    historical_data = clean_data(historical_data)
                    with open(file, 'w') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Open', 'High', 'Low', 'Close', 'Volume', 'Date'])
                        for index, row in historical_data.iterrows():
                            writer.writerow([row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row.name.strftime("%Y-%m-%d %H:%M:%S")])
            print("Successfully updated the historical data.")
        await asyncio.sleep(60)


def clean_data(dataframe):
    # Check for missing or null values
    missing_values = dataframe.isnull().sum()
    if any(missing_values):
        print(f"Missing values found in the following columns: {missing_values[missing_values > 0]}")
        # decide how to handle missing values
        dataframe = dataframe.dropna()
        print("Missing values have been removed")
    else:
        print("No missing values found")
    # Check for errors in the data
    for col in dataframe.columns:
        if dataframe[col].dtype == 'float64':
            # check if any value is NaN
            if dataframe[col].isnull().any():
                print(f"Found NaN values in the column {col}")
                # decide how to handle NaN values
                dataframe[col].fillna(dataframe[col].mean(), inplace=True)
                print("NaN values have been replaced with the mean of the column")
    print("Data cleaning completed")
    return dataframe


def load_data(ticker):
    filename = os.path.join(os.getcwd(), "data/historical_price_data", f"{ticker}.csv")
    data = pd.read_csv(filename)
    return data


def get_latest_data(ticker):
    data = load_data(os.path.join(os.getcwd(), "data/historical_price_data", f"{ticker}.csv"))
    return data.tail(1)


def get_data_by_date(ticker, date):
    data = load_data(os.path.join(os.getcwd(), "data/historical_price_data", f"{ticker}.csv"))
    return data[data["date"] == date]


def get_data_by_range(ticker, start_date, end_date):
    data = load_data(os.path.join(os.getcwd(), "data/historical_price_data", f"{ticker}.csv"))
    mask = (data["date"] >= start_date) & (data["date"] <= end_date)
    return data[mask]

import asyncio
import data_collection_hist_data as a
import pandas as pd
import matplotlib.pyplot as plt
import time


def main():
    ticker = "AAPL"
    start_date = None
    end_date = None
    time_frame = 'max'
    historical_data = a.get_historical_data(ticker, start_date=start_date, end_date=end_date, time_frame=time_frame)
    a.save_data_to_csv(historical_data, f"{ticker}.csv")

    while True:
        asyncio.run(a.update_historical_data())
        latest_data = a.load_data(ticker)
        plt.plot(latest_data['Close'])
        plt.show()
        time.sleep(180)


if __name__ == "__main__":
    main()


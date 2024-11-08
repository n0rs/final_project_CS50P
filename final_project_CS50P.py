import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
import csv

# dictionary of possible timeframes for data acquisition
time_series = {
    "intraday": "TIME_SERIES_INTRADAY",  # daily data of last 2 month
    "daily": "TIME_SERIES_DAILY",  # daily data of 20+ years
    "weekly": "TIME_SERIES_WEEKLY",  # weekly data of 20+ years
    "monthly": "TIME_SERIES_MONTHLY",  # monthly data of 20+ years
}

# creating list of all available equities of this API using the api for all traded equities on last business day
try:
    listed_equities = requests.get('https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=&apikey=MEPQ0O61XY\
MONWTH')
except requests.RequestException:
    pass

eq = listed_equities.content.decode('utf-8')
ae = csv.reader(eq.splitlines(), delimiter=",")
equities_list = list(ae)

with open("active_equities_last_business_day.csv", "w", newline="") as filename:
    scripter = csv.writer(filename, delimiter=",")
    scripter.writerows(equities_list)

# list to check if equity is available
active_short = []

# list used for full name of equity during plotting
active_full = []
with open("active_equities_last_business_day.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        active_short.append(row[0])
        active_full.append(row[1])


def main():
    equity = get_equity()
    frequency = get_frequency()
    url = make_url(frequency, equity)
    plot_data(url, frequency, equity)


def get_equity():
    while True:
        equity = input("what stock would you like to analyze? ").casefold().strip()
        # checking if equity of user is in list of available equities of the API
        if equity.upper() in active_short:
            return equity
        else:
            print("Not a valid equity!")
            pass


def get_frequency():
    while True:
        # asking for timeframe of data
        frequency = input("How much data do you want to get?\n"
                          "Options: \n"
                          "Enter: intraday, daily, weekly, monthly or help for more info\n").casefold().strip()
        if frequency == "help":
            help = get_helpf()
            if help == "ok":
                pass
            else:
                sys.exit("User chose to exit")
        elif frequency in time_series.keys():
            return frequency
        else:
            print("That´s not a valid frequency!")
            pass


def make_url(fre, e):
    try:
        # generating the URL
        # intraday timeframe requires additional argument of how long the interval between each data point should be
        if fre == "intraday":
            while True:
                try:
                    interval = int(input("What time between two data-points? \n"
                                         "options:\n"
                                         "1, 5, 15, 30, 60 (in minutes)\n"))
                    if interval in [1, 5, 15, 30, 60]:
                        # if all requirements are checked, URL is generated with simple f-string
                        url = requests.get(f'https://www.alphavantage.co/query?function={time_series[fre]}&datatype=csv\
&symbol={e.upper()}&interval={interval}min&apikey=MEPQ0O61XYMONWTH')
                        return url
                    else:
                        print("Not a valid interval.")
                        pass
                except (ValueError, requests.RequestException):
                    pass
        else:
            url = requests.get(f'https://www.alphavantage.co/query?function={time_series[fre]}&datatype=csv&symbol=\
{e.upper()}&apikey=MEPQ0O61XYMONWTH')
            return url
    except requests.RequestException:
        pass


def get_helpf():
    print()
    print("intraday: daily data of last 2 month\n"
          "daily: daily data of 20+ years\n"
          "weekly: weekly data of 20+ years\n"
          "monthly: monthly data of 20+ years\n")
    ok = input("Enter ok to proceed, leave to exit: ")
    return ok


def plot_data(url, fre, e):
    # index number of wanted equity; used for plot title and csv file name
    index = active_short.index(f"{e.upper()}")

    # reading csv file acquired through requests.get
    r = url.content.decode('utf-8')
    data = csv.reader(r.splitlines(), delimiter=",")

    # storing data in a list to write a csv file which can be saved on users pc
    data_list = list(data)

    # saving csv file
    with open(f"{active_full[index]}_{fre}.csv", "w") as file:
        writer = csv.writer(file, delimiter=",")

        # write 1 row so headers stay the same
        writer.writerow(data_list[0])

        # writing following rows in reverse order so the oldest data point is in the first row
        writer.writerows(reversed(data_list[1:]))

    # plotting data
    stock_data = f"{active_full[index]}_{fre}.csv"
    columns = ["timestamp", "close"]
    df = pd.read_csv(stock_data, usecols=columns)
    df.set_index("timestamp").plot()
    plt.xlabel("timestamp")
    plt.ylabel("Price ($)")
    plt.locator_params(axis="x", nbins=7)
    plt.legend([f"{e.upper()}"])
    plt.title(f"{fre.title()} stock prices of {active_full[index]}")
    plt.show()
    plt.savefig(f"{active_full[index]}_{fre}.png")


if __name__ == "__main__":
    main()
import sys
import argparse
from stock import Fetcher
from stock import Query
from stock import Tickers
"""
Should have a main module that takes the following flags:
∗ operation: Values are: ’Fetcher’, ’Ticker’, or ’Query’ Based on the value of 
    this variable, you will decide which class you will instantiate and
    the optional arguments whose values you will need.

1. For ’Ticker’: Use the optional flag ’ticker count’ to instantiate Tickers 
    class and then call the save tickers() function.

2. For ’Fetcher’: Use the optional flags ’db’ and ’time limit to instantiate 
    Fetcher class and then call the fetch all data() function.

3. For ’Query’: Use the optional flags ’db’ and ’time’ and ’ticker’ to 
    instantiate Query class and then call the function to fetch and print data 
    from the database. The data must be printed out to the terminal when this 
    operation is used.

∗ time: Used by the Query class to identify the specific minute for which to 
    print data. Optional argument used only for the Query class.

∗ ticker: Used by the Query class to identify the specific ticker for which 
    to print data. Optional argument used only for the Query class.

∗ time limit: Used by the Fetcher class to identify the length of time in 
    seconds for which to fetch data. Optional argument used only for 
    the Fetcher class.
∗ db: Used by the Fetcher and Query classes to specify the database file to be 
    used. Optional argument used only for the Fetcher and Query classes.

∗ ticker count: Used only by the Tickers class to specify the number of 
    valid tickers to be fetched. Optional argument only used by Tickers class.
"""

def parse_args(args):
    """ Configure parsing of command line arguments """
    parser = argparse.ArgumentParser(description=(f"Prints details corresponding to ticker"
        " and specific time"))

    parser.add_argument("--operation", nargs='?', default=None, type=str, 
        help="operation parameter for class selection")
    parser.add_argument("--ticker_count", nargs='?', default=None, type=str, 
        help="parameter to specify the number of valid tickers to be fetched")
    parser.add_argument("--time_limit", nargs='?', default=None, type=str, 
        help="parameter for update time limit for Fetcher class")
    parser.add_argument("--time", nargs='?', default=None, type=str, 
        help="parameter to identify the specific minute for which to print data.")
    parser.add_argument("--ticker", nargs='?', default=None, type=str, 
        help="ticker: Used by the Query class to identify the specific ticker"
        "for which to print data")
    parser.add_argument("--db", nargs='?', default=None, type=str, 
        help="parameter to specify the database file to be used.")

    args = parser.parse_args(args)
    return args    

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    d = vars(args)
    if d["operation"]=="Ticker" and d["ticker_count"]!=None:
         tickers = Tickers(int(d["ticker_count"]))
         tickers.save_tickers()
         
    elif d["operation"]=="Fetcher" and d["time_limit"]!=None and d["db"]!=None:
         fetcher = Fetcher(int(d["time_limit"]),d["db"])
         fetcher.fetch_all_data()

    elif d["operation"]=="Query" and d["time"]!=None and d["db"]!=None and d["ticker"]!=None:
        query = Query(d["time"],d["db"],d["ticker"])
        query.find_symbol()

    else:
        print("What you entered was not valid")

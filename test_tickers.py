import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(THIS_FOLDER+'/../')
from stock import Tickers
from pathlib import Path
import requests


def test_save_tickers():
    """
    Test function for Tickers.save_tickers()
    checks if file exists after file save 
    """

    tick = Tickers(100)
    tick_test = Tickers(130)
    tick_test.save_tickers()
    tick.save_tickers()
    symbols = []
    test_symbols = []
    my_file = Path('./tickers.txt')
    assert my_file.exists()
    
def test_get_tickers():
    """
    Test function for Tickers.get_tickers()
    checks if the file has the requested number of tickers within it
    """
    tick = Tickers(100)
    headers = {'Accept-Encoding': 'identity'}
    r = requests.get("http://www.nasdaq.com/screening/companies"
    "-by-industry.aspx?exchange=NASDAQrender=download",headers=headers)
    ticker_list = tick.get_tickers(r)
    assert len(ticker_list) == 100


def test_confirm_ticker():
    """
    Test function for Tickers.confirm_tickers()
    confirms if requested tickers are valid NASDAQ ticker symbols
    """
    tick = Tickers(100)
    assert tick.confirm_ticker("YI") == True
    assert tick.confirm_ticker("Gucci") == False


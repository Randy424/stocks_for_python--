import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(THIS_FOLDER+'/../')
from stock import Tickers
from pathlib import Path
import requests


def test_save_tickers():
    tick = Tickers(100)
    tick_test = Tickers(130)
    tick_test.save_tickers()
    tick.save_tickers()
    symbols = []
    test_symbols = []
    my_file = Path('./tickers.txt')
    assert my_file.exists()
    
def test_get_tickers():
    tick = Tickers(100)
    headers = {'Accept-Encoding': 'identity'}
    r = requests.get("http://www.nasdaq.com/screening/companies"
    "-by-industry.aspx?exchange=NASDAQrender=download",headers=headers)
    ticker_list = tick.get_tickers(r)
    assert len(ticker_list) == 100


def test_confirm_ticker():
    tick = Tickers(100)
    assert tick.confirm_ticker("YI") == True
    assert tick.confirm_ticker("Gucci") == False


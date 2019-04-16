import sys
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER+'/../')
import tickers


def test_ticker():
    tick = tickers.Tickers(100)
    tick.save_tickers()
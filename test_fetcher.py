import sys
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER+'/../')
from stock import Fetcher

def test_fetcher():
    """
    Test function for Fetcher.fetch_all_data()
    Will check to see that fetch_all_data is returning True
    """
    fetch = Fetcher(10,"stocks.db")
    assert fetch.fetch_all_data()
import sys
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER+'/../')
from stock import Fetcher

def test_fetcher():
    """
    Test function for query.find_symbol()

    Will assume that we have a database ”stocks.db” 
    that has data for the ’YI’ ticker at time '16:32'
    """
    fetch = Fetcher(10,"test.db")
    fetch.fetch_all_data()
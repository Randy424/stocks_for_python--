import sys
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER+'/../')
from stock import Fetcher
from stock import Query

def test_fetcher():
    """
    Test function for Fetcher.fetch_all_data()
    Will check to see that fetch_all_data is logging a ticker value at
    the current time.

    Potential edge case for test failure if fetch.get_time and fetch_all_data
    are executed as the minute value for our current time changes
    """
    fetch = Fetcher(10,"stocks.db")
    time = fetch.get_time()
    fetch.fetch_all_data()
    
    query = Query(time,"stocks.db","YI")
    result = query.find_symbol()
    comp = time = 'Time: '+time
    assert comp == result[0]

if __name__ == '__main__':
    test_fetcher()


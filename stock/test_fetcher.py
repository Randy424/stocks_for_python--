import sys
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER+'/../')
import fetcher

def test_fetcher():
    fetch = fetcher.Fetcher(10,"test.db")
    fetch.fetch_all_data()
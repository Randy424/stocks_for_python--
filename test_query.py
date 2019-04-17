import sys
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER+'/../')
from stock import Query as q

def test_find_symbol():
    """
    Test function for query.find_symbol()
    Will assume that we have a database ”stocks.db” 
    that has data for the ’YI’ ticker at time '16:32'
    """
    query = q("16:32","stocks.db","YI")
    
    info = query.find_symbol()

    assert info == ['Time: 16:32', 'Ticker: YI', 'Low: 5.82', 'High: 6.58',
    'Open: 5.82', 'Close: 6.49', 'Price: 6.49', 'Volume: 31101']

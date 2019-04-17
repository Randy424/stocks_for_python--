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
    query = q("11:25","test.db","ADAP")
    
    info = query.find_symbol()

    print(info)

if __name__ == '__main__':
    test_find_symbol()
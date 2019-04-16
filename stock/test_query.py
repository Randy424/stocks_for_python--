import sys
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER+'/../')
import query as q

def test_query():
    query = q.Query("01:00","test.db","ADAP")
    query.find_symbol()
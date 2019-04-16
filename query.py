import sys
import sqlite3

class Query:
    """
    This class searches for a specified ticker/time combination and returns
    all associated data
    """
    def __init__(self, time, db, ticker):
        """
        Creates the variables needed for this class

        :type time: string
        :param time: the time to search for

        :type db: sqlite3.connect
        :param db: establishes a connectino to the database file

        :type db_name: string
        :param db_name: the database file to access

        :type ticker: string
        :param ticker: the ticker to search for
        """
        self.time = time
        self.db = sqlite3.connect(db)
        self.db_name = db
        self.ticker = ticker

    def find_symbol(self):
        """
        Runs the select function within the database to quickly find
        the ticker/time combination
        Prints out the associated values
        """
        selector = self.db.cursor()
        selector.execute("SELECT * FROM StockData WHERE Ticker ="
                        +"'"+self.ticker+"'"+
                        " AND Time ="+"'"+self.time+"'")
        labels = list(map(lambda x: x[0], selector.description))
        values = list(selector.fetchone())
        for label,value in zip(labels,values):
            print(label+": "+value)
        return label+": "+value

        #if verbose == "True":
        #    print(f"Number of rows: {numrows} (not counting row of labels)")
        #    print(f"Number of columns: {len(fields[0])}")
        #    print(' '.join(field for field in fields[0]))


if __name__ == "__main__":
    query = Query("11:25","test.db","ADAP")
    query.find_symbol()

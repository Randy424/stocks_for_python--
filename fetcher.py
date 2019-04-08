import os
import sys
import csv
import sqlite3
import pandas as pd
import datetime
import time
from iex import Stock

class Fetcher:
    def __init__(self,time_limit,db):
        self.last_ticker_values = {}
        self.time_lim = time_limit
        self.db_name = db
        self.db = sqlite3.connect(db)

    def fetch_all_data(self):
        """
        Loads tickers from tickers.txt
        if info.csv does not already exist it is created with header
        Calls updater over span of time_lim

        args:
        time_lim - int

        """
        c = self.db.cursor()
        if (os.path.isfile(self.db_name) == False):
            c.execute("""CREATE TABLE tickers (
                    Time text,
                    Ticker text,
                    LatestPrice text,
                    LatestVolume text,
                    Close text,
                    Open text,
                    Low text,
                    High text
                    )""")
        t_end = time.time() + self.time_lim
        while time.time() < t_end:
            iter_start = datetime.datetime.now()
            f = open("tickers.txt", 'r')

            #Enter file and grab tickers one by one to update them
            for l in f:
                l = l.strip()
                self.write_update(l,c)

            #sleeps the program until the current minute ends
            now = datetime.datetime.now()
            if iter_start.hour == now.hour and iter_start.minute == now.minute:
                time.sleep(60-now.second)
        self.db.commit()
        self.db.close()

    def write_update(self,ticker,connection):
        """
        Is called from gettickers_callupdate()
        Gets current stock quote using ticker (ticker symbol as string)
        if ticker exists in pdf, updates ticker, if not, it appends current quote
        data is saved via overwriting previous info.csv 

        args: ticker - string

        """
        headers = ["symbol","latestPrice","latestVolume","close","open","low","high"]
        #most recent ticker time is stored in dictionary for faster checking
        if ticker in self.last_ticker_values:
            if self.last_ticker_values[ticker] == get_time():
                return

        #Grabs stock information for a ticker and adds it to the dataframe
        book = self.get_book(ticker)
        values = []
        values.append("'"+self.get_time()+"'")
        for header in headers:
            values.append("'"+str(book[header])+"'")
        values = ",".join(values)
        command ="INSERT INTO tickers VALUES (" + values + ")"
        connection.execute(command)

        #updates ticker value in its dictionary
        self.last_ticker_values[ticker] = self.get_time()

    def get_time(self):
        """
        returns time in needed format for csv
        """
        currentDT = datetime.datetime.now()
        return currentDT.strftime('%H:%M')

    def get_book(self,ticker):
        """
        returns stock information in the form of a dicitonary
        """
        book = Stock(ticker).quote()
        return book

if __name__ == '__main__':
    fetcher = Fetcher(10,"test.db")
    fetcher.fetch_all_data()


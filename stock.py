import os
import sys
import csv
import sqlite3
import pandas as pd
import datetime
import time
from iex import Stock
import json
import pandas as pd 
import requests
import re

class Tickers:
    """
    This class grabs n amount of tickers using the iex Stock function
    """
    def __init__(self,ticker_count,output_file="tickers.txt"):
        """
        Creates the variables needed for the class

        :type ticker_count: int
        :param ticker_count: the amount of tickers to grab

        :type output_file: string
        :param output_file: destination to store tickers in.
                            Defaults as tickers.txt
        """
        self.n = ticker_count
        self.output_file = output_file

    def save_tickers(self):
       """ 
       Sends get request to url, calls get_tickers to #parses html, 
       and return 'n' tickers. 
       If tickers.txt does not already exist, function creates
       it; otherwise it is appended to. 
       Appends tickers, one per line. 
       Returns the get request text body. 
       """

       headers = {'Accept-Encoding': 'identity'}
       r = requests.get("http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQrender=download",headers=headers)

       valid_ticker_list = self.get_tickers(r)
       #if the length of valid tickers is greater than 0, move the list into
       #a file
       if(len(valid_ticker_list) > 0):
          f = open(self.output_file, "w+")

          for i in valid_ticker_list:
               f.write( f"{i.upper()} \n")
          f.close()
       else:
          print("requesting too many tickers, n =< 150")
       return r

    def get_tickers(self,html):
       """
       Parses html from request.get() output
       returns list of 'n' many tickers. Returns
       an empty list if the requested number of tickers
       is greater than 110

       :type html: string
       :param html: the html address to go to for the nasdaq
       """
       ticker_list = []
       #if n > limit, returns empty list
       if self.n > 110:
          return ticker_list

       #isolating ticker from url
       results = re.findall(r'/symbol/.*" ', html.text)

       #check tickers loop and grab more tickers if needed
       priorurl = html
       while len(ticker_list)<self.n:
           for i in results:
               temp = i.split("\"")
               splitr = temp[0].split('/')
               ticker = splitr[2]
               if self.confirm_ticker(ticker):
                   ticker_list.append(ticker)
               if len(ticker_list) == self.n:
                   break
           #If found all valid tickers, break
           if len(ticker_list) == self.n:
               break
           #Else, grab the next page of tickers from nasdaq
           else:
               newstart = len(results)
               nexturl = re.findall(r"https://.*id=\Wmain_content_lb_NextPage",priorurl.text)
               nurl_list = nexturl[0].split()
               nextpage = nurl_list[len(nurl_list)-2]
               nextpage = re.findall(r'https://.*[^"]',nextpage)
               nexturl = requests.get(nextpage[0])
               priorurl=nexturl
               results+=re.findall(r'/symbol/.*" ', nexturl.text)
               results = results[newstart::]
       return ticker_list

    def confirm_ticker(self,t):
       """
       Uses iex.Stock().price to check if a ticker has a listed price

       :type t: string
       :param t: a ticker symbol
       """
       try:
          #blocking std output from Stock().price()
          self.blockPrint()

          #checking if ticker has price
          Stock(t).price()

          #Restoring std output
          self.enablePrint()

          return True
       except:
          #print("Unexpected error:", sys.exc_info()[0])
          #print(f"Ticker: {t} not found")
          return False


    def blockPrint(self):
       """
       Disable stdoutput
       """
       sys.stdout = open(os.devnull, 'w')

    def enablePrint(self):
       """
       Restore stdoutput
       """
       sys.stdout = sys.__stdout__



class Fetcher:
    """
    This class updates stock information for n amount of seconds and stores
    data in a db file
    """
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
        c.execute("""CREATE TABLE IF NOT EXISTS StockData (
                Time text,
                Ticker text,
                Price text,
                Volume text,
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
        headers = ["symbol","Price","Volume","close","open","low","high"]
        #most recent ticker time is stored in dictionary for faster checking
        if ticker in self.last_ticker_values:
            if self.last_ticker_values[ticker] == self.get_time():
                return

        #Grabs stock information for a ticker and adds it to the dataframe
        book = self.get_book(ticker)
        values = []
        values.append("'"+self.get_time()+"'")
        for header in headers:
            values.append("'"+str(book[header])+"'")
        values = ",".join(values)
        command ="INSERT INTO StockData VALUES (" + values + ")"
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
        selfg = sqlite3.connect(db)
        self.db_name = db
        self.ticker = ticker

    def find_symbol(self):
        """
        Runs the select function within the database to quickly find
        the ticker/time combination
        Prints out the associated values
        """
        result_out = []
        selector = self.db.cursor()
        selector.execute("SELECT * FROM StockData WHERE Ticker ="
                        +"'"+self.ticker+"'"+
                        " AND Time ="+"'"+self.time+"'")
        labels = list(map(lambda x: x[0], selector.description))
        values = list(selector.fetchone())
        for label,value in zip(labels,values):
            print(label+": "+value)
            result_out.append(label+": "+value)

        return result_out

        #if verbose == "True":
        #    print(f"Number of rows: {numrows} (not counting row of labels)")
        #    print(f"Number of columns: {len(fields[0])}")
        #    print(' '.join(field for field in fields[0]))


#!/usr/bin/python

import json
import pandas as pd 
import requests
import re
from iex import Stock
import os
import sys

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
          if (os.path.isfile(self.output_file)):
             f = open(self.output_file, "a+")
          else:
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


if __name__=="__main__":
   tickers = Tickers(100)
   tickers.save_tickers()


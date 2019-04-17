.. Stocks For Python-- documentation master file, created by
   sphinx-quickstart on Wed Apr 10 22:44:56 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Stocks For Python--
==============================
This is a project designed to gather stock information from the Nasdaq for at
most 110 ticker symbols. This stock information is then stored in a sqlite3
database for future use. You can quickly data lookups for a ticker symbol
at a specific time with our query module which returns all stock information
for that ticker and time combination.

Requirements:
	Python3
	iex-api-python

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   tutorial
   classes
   test_fetcher
   test_tickers
   test_query
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

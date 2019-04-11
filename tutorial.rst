Tutorial
===================

The following is a quick tuturial on how to use this project. 

From a terminal, run one of the following commands:
	>>> python3 driver.py --operation=Ticker --ticker_count=100
		
		This runs the driver module and tells it to create a Tickers object.
		The Ticker object will then run a command called "save_tickers()"
		which grabs the first 100 valid tickers and saves them in a text file
		called tickers.txt
	
	>>> python3 driver.py --operation=Fetcher --time_limit=300 --db="stocks_new.db"
		
		This runs the driver module and tells it to create a Fetcher object. 
		The Fetcher object performs a function called "fetch_all_data()"
		This function grabs the tickers stored in tickers.txt and uses the
		iex module's "Stock" function to get data for the amount of seconds
		specified in time_limit. Every minute, a new entry is inserted into 
		the specified database for each ticker
		
	>>> python3 driver.py --operation=Query --time=15:11 --db="stocks_new.db" --ticker="YI"
		
		This runs the driver module and tells it to create a Query object
		Query performs a function called "find_symbol()" which searches for an
		occurance of the specified ticker with the specified time in the 
		db file. Afterwards, all stock information associated with the 
		ticker/time combination is printed out		

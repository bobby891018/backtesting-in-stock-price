Backtesting a simple trading strategy by using the historical prices of 
Yuanta/P-shares Taiwan Top 50 ETF (元大台灣50 - 0050) in Taiwan stock market.

(1) Read the OHLCV data frame from 'OHLCV.csv' file. 
The file includes data of 400 trading days start from 7 Oct 2020.

(2) Define the trading strategy (MovingAverageCrossStrategy), which will generate moving-averaged data from short and long filter windows.
The values have been set to defaults of 5 days and 20 days, respectively.
The trading strategy will output the signal as 1 while the short moving-averages of prices crossover the long moving-averages, and vice versa


(3) Create a portfolio with an initial capital of NTD 100,000. 
Assuming that we buy (or sell) 1000 shares in each time. 


![image](https://github.com/bobby891018/modified-backtesting-in-stock-price/blob/main/Figure.png)
[Upper panel] Moving average crossover performance from our data. 
Upward (downward) triangle symbols denote the buying (selling) signals.

[Lower panel] The returns of our portfolio. 
By following this strategy, we may made a profit of ~30% in these 400 trading days.


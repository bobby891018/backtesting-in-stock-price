from ReadOut import *

class MovingAverageCrossStrategy(object):
    """    
    Requires:
    data - A OHLCV DataFrame.
    short_window - Lookback period for short moving average.
    long_window - Lookback period for long moving average."""

    def __init__(self, data, short_window=5, long_window=20):
        self.data = data
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        """Returns the DataFrame of symbols containing the signals
        to go long, short or hold (1, -1 or 0)."""
        signals = pd.DataFrame(index=self.data.index)
        signals['signal'] = 0.0

        ''' Create the set of short and long simple moving averages over the 
        respective periods'''
        signals['short_mavg'] = SMA(self.data.close, self.short_window)
        signals['long_mavg'] = SMA(self.data.close, self.long_window)

        ''' Create a 'signal' (invested or not invested) when the short
        moving average crosses the long moving average, but only for
        the period greater than the shortest moving average window'''
        signals.signal[self.short_window:] = np.where(
            signals.short_mavg[self.short_window:] 
            > signals.long_mavg[self.short_window:], 1.0, 0.0)   

        ''' Take the difference of the signals in order to
        generate actual trading orders'''
        signals['position'] = signals.signal.diff()   

        return signals

class Portfolio(object):
    """Inherits Portfolio to create a system that purchases 100 units of 
    a particular symbol upon a long/short signal, assuming the market 
    open price of a bar.

    In addition, there are zero transaction costs and cash can be immediately 
    borrowed for shorting (no margin posting or interest requirements). 

    Requires:
    data - A OHLCV DataFrame.
    signals - A pandas DataFrame of signals (1, 0, -1) for each symbol.
    initial_capital - The amount in cash at the start of the portfolio."""

    def __init__(self, data, signals, initial_capital=100000):
        self.data = data
        self.signals = signals
        self.initial_capital = float(initial_capital)
        self.trades = self.generate_trades()
        
    def generate_trades(self):
        """Creates a 'trades' DataFrame that simply longs or shorts
        1000 of the particular symbol based on the forecast signals of
        {1, 0, -1} from the signals DataFrame."""
        trades = pd.DataFrame(index=self.signals.index).fillna(0.0)
        trades['trade'] = 1000*self.signals.signal
        return trades
                    
    def backtest_portfolio(self):
        """Constructs a portfolio from the positions DataFrame by 
        assuming the ability to trade at the precise market open price
        of each bar (an unrealistic assumption!). 

        Calculates the total of cash and the holdings (market price of
        each position per bar), in order to generate an equity curve
        ('total') and a set of bar-based returns ('returns').

        Returns the portfolio object to be used elsewhere."""

        ''' Construct the portfolio DataFrame to use the same index
        as 'trade' and with a set of 'trading orders' in the
        pos_diff' object, assuming market open prices. '''
        portfolio = pd.DataFrame(index=self.data.index)
        pos_diff = self.trades.trade.diff()

        '''Create the 'holdings' and 'cash' series by running through
        the trades and adding/subtracting the relevant quantity from
        each column '''
        portfolio['holdings'] = self.trades.trade*self.data.open
        portfolio['cash'] = self.initial_capital-(pos_diff*self.data.open).cumsum()

        ''' Finalise the total and bar-based returns based on the 'cash'
        and 'holdings' figures for the portfolio '''
        portfolio['total'] = portfolio.cash + portfolio.holdings
        portfolio['returns'] = portfolio.total.pct_change()
        return portfolio

#daily_trading = read_daily_trading('0050', 400)
daily_trading = pd.read_csv('/Users/bobby/Desktop/OHLCV.csv')
signals = MovingAverageCrossStrategy(daily_trading).generate_signals()
portfolio = Portfolio(daily_trading, signals).backtest_portfolio()


if __name__ == "__main__":
    fig = plt.figure()
    ax1 = fig.add_subplot(211,  ylabel='Price in NTD')

    ''' plot the closing price overlaid with the moving averages'''
    daily_trading.close.plot(ax=ax1, color='r', lw=2.)
    signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

    ''' plot the "buy" trades against prices '''
    ax1.plot(signals.loc[signals.position == 1.0].index, 
             signals.short_mavg[signals.position == 1.0],
             '^', markersize=10, color='m')

    ''' plot the "sell" trades against prices '''
    ax1.plot(signals.loc[signals.position == -1.0].index, 
             signals.short_mavg[signals.position == -1.0],
             'v', markersize=10, color='k')
    ax1.axes.xaxis.set_visible(False)

    ''' plot the equity curve'''
    ax2 = fig.add_subplot(212, ylabel='Portfolio returns (per 10k NTD)')
    portfolio.returns.cumsum().plot(ax=ax2, lw=2.)

    ''' plot the "buy" and "sell" trades against the equity curve '''
    ax2.plot(portfolio.loc[signals.position == 1.0].index, 
             portfolio.returns.cumsum()[signals.position == 1.0],
             '^', markersize=10, color='m')
    ax2.plot(portfolio.loc[signals.position == -1.0].index, 
             portfolio.returns.cumsum()[signals.position == -1.0],
             'v', markersize=10, color='k')
    plt.show()












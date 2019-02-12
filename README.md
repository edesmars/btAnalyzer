# PipsArtist - Backtrader Analyzers

This repository is a set of analyzer for backtrader that helps review a strategy. These analyzers have been made for Forex strategies is mind but may be used for other instruments.

__This repository is under heay development and is not production ready__

## Analyzer available

### ForexTrades
This is a simple Analyzer that keeps track of all trades closed. It can be used for live or backtesting.
It allows to keep track of:

* Trade closed position (Buy or Sell)
* Profit in absolute value and pips
* Open and Close datetime
* Open and Close price
* Maximum drawback in pips
* Maximum profit in pips

### ForexStats
This Analyzer is using the output of ``ForexTrades`` Analyzer to give details about the strategy including:
It returns several analysis for a strategy in 4 different areas:

1. Overal strategy (For full period of trading or backtesting)
    * Gross Profit
    * Gross Profit (pips)
    * Gross Loss
    * Gross Loss (pips)
    * Net Profit
    * Net Profit (pips)
    * Profit Factor
    * Expected Payoff
3. Total
    * Total Number of Trades
    * Total Won 
    * Percentage of won
    * Total Loss
    * Percentage of loss
    * Average Trade profit in absolute value
    * Average Trade profit in pips
    * Max Profit in absolute value
    * Max Profit in pips
    * Average Loss in absolute value
    * Average Loss in pips
    * Max Loss in absolute value
    * Max Loss in pips
4. Short Trades
    * Same as for Total but only for short trades
5. Long Trades
    * Same as for Total but only for long trades
6. Streak - Win and Loss Streak with the following for each:
    * Max number of trades in a streak
    * Average number of trades in a streak
    * Max Profit/Loss in absolute value
    * Max Profit/Loss in pips
    * Average Profit/Loss in absolute value
    * Average Profit/Loss in pips

## Known Limitation

These analyzers have only been tested with Currencies and with a 4/5 digits currencies.
It does not support 2/3 digits currencies such as USD/JPY
    
## Requirements

* python 3.6+
* Backtrader
* Pandas
* pipenv

## Installation

1. Clone this repository ``git clone git@github.com:edesmars/btAnalyzer.git``
2. Go into the newly created directory: ``cd btAnalyzer`` 
2. Install dependencies. Pipenv is recommended: ``pipenv --python 3.6 && pipenv install`` or use ``pip install``
2. In your backtrader script, add a new path to be able to import these Analyzers
```python
import sys
sys.path.append('/path/to/clone')

import bt_analyzers

```
3. Add the analyzers into your cerebro instance
```python
cerebro.addanalyzer(bt_analyzer.stats.ForexStats)
```

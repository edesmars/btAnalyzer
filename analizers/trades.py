from backtrader import Analyzer
import json

class ForexTrades(Analyzer):

    OP_BUY, OP_SELL = range(2)

    def __init__(self):
        super(ForexTrades, self).__init__()
        self._forextrades = []

    def notify_trade(self, trade):

        if trade.justopened:
            self._forextrades.append({
                "ref": trade.ref,
                "type": self.OP_BUY if trade.size > 0 else self.OP_SELL,
                "open_price": trade.price,
                "size": trade.size,
                "close_price": 0.0,
                "profit": 0.0,
                "min_price": trade.price,
                "max_price": trade.price,
                "status": trade.status
            })

        if trade.isclosed:
            current_trade = list(filter(lambda x: x["ref"] == trade.ref, self._forextrades))
            current_trade = current_trade[0]
            current_trade["close_price"] = self.datas[0].close[0]
            current_trade["profit"] = trade.pnlcomm
            current_trade["close_datetime"] = trade.close_datetime().isoformat()
            current_trade["open_datetime"] = trade.open_datetime().isoformat()

            if current_trade["type"] == self.OP_BUY:
                current_trade["profit_pips"] = (current_trade["close_price"] - current_trade["open_price"]) * 10000.0

                current_trade["max_drawdown_pips"] = ((current_trade["open_price"] - current_trade["min_price"]) * 10000.0)
                current_trade["max_profit_pips"] = (current_trade["max_price"] - current_trade["open_price"]) * 10000.0

                if current_trade["profit_pips"] != 0:
                    price_per_pips = current_trade["profit"] / current_trade["profit_pips"]
                    current_trade["max_drawdown"] = current_trade["max_drawdown_pips"] * price_per_pips
                    current_trade["max_profit"] = current_trade["max_profit_pips"] * price_per_pips
                else:
                    current_trade["max_drawdown"] = 0
                    current_trade["max_profit"] = 0

            else:
                current_trade["profit_pips"] = (current_trade["open_price"] - current_trade["close_price"]) * 10000.0

                current_trade["max_drawdown_pips"] = (current_trade["max_price"] - current_trade["open_price"]) * 10000.0
                current_trade["max_profit_pips"] = (current_trade["open_price"] - current_trade["min_price"]) * 10000.0

                if current_trade["profit_pips"] != 0:
                    price_per_pips = current_trade["profit"] / current_trade["profit_pips"]
                    current_trade["max_drawdown"] = current_trade["max_drawdown_pips"] * price_per_pips
                    current_trade["max_profit"] = current_trade["max_profit_pips"] * price_per_pips
                else:
                    current_trade["max_drawdown"] = 0
                    current_trade["max_profit"] = 0

    def next(self):
        if len(self._forextrades) > 0:
            # get all opened trades (open status = 1)
            current_trades = list(filter(lambda x: x["status"] == 1, self._forextrades))
            for trade in current_trades:
                if self.datas[0].high[0] > trade["max_price"]:
                    trade["max_price"] = self.datas[0].high[0]
                if self.datas[0].low[0] < trade["min_price"]:
                    trade["min_price"] = self.datas[0].low[0]

    def get_analysis(self, format=None):
        if format == "json":
            return json.dumps(self._forextrades)
        return self._forextrades


import pandas as pd
import numpy as np

from backtrader import Analyzer
from .trades import ForexTrades

class ForexStats(Analyzer):

    OP_BUY, OP_SELL = range(2)

    def __init__(self):
        super(ForexStats, self).__init__()
        self._forextrades = []
        self._tradeanalysis = {
            "total": {},
            "short": {},
            "long": {},
            "streak": {}
        }
        self.tradeAnalyzer = ForexTrades()
        self._streak_id = None

    def stop(self):
        self._forextrades = self.tradeAnalyzer.get_analysis()
        df = pd.DataFrame(self._forextrades)
        #remove non closed trades
        df = df.dropna()
        if len(df.index) == 0:
            return

        # TOTAL
        total = self._analyze_dataframe(df, "all")


        #SHORT
        df_short = df[df["type"] == 1]
        short_total = self._analyze_dataframe(df_short, "short")

        #LONG
        df_long = df[df["type"] == 0]
        long_total = self._analyze_dataframe(df_long, "long")

        #streak
        streak = self._streak_analysis(df)

        self._tradeanalysis["strategy"] = self._analyze_strategy(df)
        self._tradeanalysis["total"] = total
        self._tradeanalysis["short"] = short_total
        self._tradeanalysis["long"] = long_total
        self._tradeanalysis["streak"] = streak

    def _analyze_strategy(self, df):
        """
        Based on MT4 strategy tester results.
        https://www.mql5.com/en/articles/1486
        :param df:
        :return:
        """
        gross_profit = df[df["profit"] > 0 ]["profit"].sum()
        gross_profit_pips = df[df["profit"] > 0 ]["profit_pips"].sum()
        gross_loss = df[df["profit"] < 0 ]["profit"].sum()
        gross_loss_pips = df[df["profit"] < 0 ]["profit_pips"].sum()
        net_profit = gross_profit - (gross_loss * -1)
        profit_factor = gross_profit / (gross_loss * -1)
        TotalTrades = len(df.index)
        ProfitTrades = df[df["profit"] > 0 ]["profit"].count()
        LossTrades = df[df["profit"] < 0 ]["profit"].count()
        expected_payoff = (ProfitTrades / TotalTrades) * (gross_profit / ProfitTrades) - (LossTrades / TotalTrades) * ((gross_loss * -1) / LossTrades)
        return {
            "Gross Profit": gross_profit,
            "Gross Profit (pips)": gross_profit_pips,
            "Gross Loss": gross_loss,
            "Gross Loss (pips)": gross_loss_pips,
            "Net Profit": net_profit,
            "Net Profit (pips)": gross_profit_pips + gross_loss_pips,
            "Profit Factor": profit_factor,
            "Expected Payoff": expected_payoff
        }

    def _analyze_dataframe(self, df, type):
        total = {}
        #if empty dataframe, just return 0 for all values
        if len(df.index) == 0:
            total["trades"] = 0
            total["won"] = 0
            total["won %"] = 0
            total["lost"] = 0
            total["lost %"] = 0
            total["avg_profit"] = 0
            total["max_profit"] = 0
            total["avg_loss"] = 0
            total["max_loss"] = 0
            total["avg_profit_pips"] =0
            total["max_profit_pips"] = 0
            total["avg_loss_pips"] = 0
            total["max_loss_pips"] = 0
            return total

        total["trades"] = len(df.index)
        total["won"] = df[df["profit"] > 0]["profit"].count()
        total["won %"] = (total["won"] / total["trades"]) * 100.0
        total["lost"] = df[df["profit"] < 0]["profit"].count()
        total["lost %"] = (total["lost"] / total["trades"]) * 100.0
        #pnl profit and loss stat in $
        total["avg_profit"] = df[df["profit"] > 0]["profit"].mean()
        total["max_profit"] = df[df["profit"] > 0]["profit"].max()
        total["avg_loss"] = df[df["profit"] < 0]["profit"].mean()
        total["max_loss"] = df[df["profit"] < 0]["profit"].min()
        #pnl profit and loss stat in pips
        total["avg_profit_pips"] = df[df["profit"] > 0]["profit_pips"].mean()
        total["max_profit_pips"] = df[df["profit"] > 0]["profit_pips"].max()
        total["avg_loss_pips"] = df[df["profit"] < 0]["profit_pips"].mean()
        total["max_loss_pips"] = df[df["profit"] < 0]["profit_pips"].min()

        return total



        return self._streak_id
    def _streak_analysis(self, dataframe):
        df = dataframe
        #win =1, loss = -1. Trades with 0 profit are considered loss trades
        df["win_flag"] = np.where(df["profit"] > 0, 1, 0)
        df["win_next"] = df["win_flag"].shift()
        df["streak"] = np.where(df["win_flag"] == df["win_next"], 0, 1)
        df["streak"] = df["streak"].cumsum()
        df_streak = df.groupby("streak").agg({
            "profit": ['sum', 'count'],
            "profit_pips": ['sum', 'count']
        })

        result = {
            "win": {
                "max": df_streak[df_streak["profit"]['sum'] > 0]["profit"]["count"].max(),
                "avg": df_streak[df_streak["profit"]['sum'] > 0]["profit"]["count"].mean(),
                "profit max": df_streak[df_streak["profit"]['sum'] > 0]["profit"]["sum"].max(),
                "profit avg": df_streak[df_streak["profit"]['sum'] > 0]["profit"]["sum"].mean(),
                "profit max (pips)": df_streak[df_streak["profit"]['sum'] > 0]["profit_pips"]["sum"].max(),
                "profit avg (pips)": df_streak[df_streak["profit"]['sum'] > 0]["profit_pips"]["sum"].mean(),
            },
            "loss": {
                "max": df_streak[df_streak["profit"]['sum'] < 0]["profit"]["count"].max(),
                "avg": df_streak[df_streak["profit"]['sum'] < 0]["profit"]["count"].mean(),
                "loss max": df_streak[df_streak["profit"]['sum'] < 0]["profit"]["sum"].min(),
                "loss avg": df_streak[df_streak["profit"]['sum'] < 0]["profit"]["sum"].mean(),
                "loss max (pips)": df_streak[df_streak["profit"]['sum'] < 0]["profit_pips"]["sum"].min(),
                "loss avg (pips)": df_streak[df_streak["profit"]['sum'] < 0]["profit_pips"]["sum"].mean(),
            }
        }
        return result

    def get_analysis(self):
        return dict(detail_trades=self._forextrades, trade_analysis = self._tradeanalysis)
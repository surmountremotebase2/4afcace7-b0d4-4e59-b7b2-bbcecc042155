from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

# trueinrow(C < C1, 5) = 5 and L < L1 and X > L1 + ((H1 - L1) / 2) with X = signal threshold
def buy_5l_close_at(data, ticker):
    close1 = data[-2][ticker]["close"]
    close2 = data[-3][ticker]["close"]
    close3 = data[-4][ticker]["close"]
    close4 = data[-5][ticker]["close"]
    close5 = data[-6][ticker]["close"]
    high = data[-1][ticker]["high"]
    low = data[-1][ticker]["low"]
    low1 = data[-2][ticker]["high"]
    high1 = data[-2][ticker]["high"]

    if close1 < close2 and close1 < close3 and close1 < close4 and close1 < close5 and low < low1:
        threshold = low1 + ((high1 - low1) / 2)
        # return threshold for confirmation if below day high
        if high > threshold:
            return threshold
        else:
            return -1.0
    else:
        return -1.0

# l = minl5 and X > L1 + ((H1 - L1) / 2) with X = signal threshold
def buy_5l_low_at(data, ticker):
    low = data[-1][ticker]["low"]
    low1 = data[-2][ticker]["low"]
    low2 = data[-3][ticker]["low"]
    low3 = data[-4][ticker]["low"]
    low4 = data[-5][ticker]["low"]
    high = data[-1][ticker]["high"]
    high1 = data[-2][ticker]["high"]

    if low < low1 and low < low2 and low < low3 and low < low4:
        threshold = low1 + ((high1 - low1) / 2)
        # return threshold for confirmation if below day high
        if high > threshold:
            return threshold
        else:
            return -1.0
    else:
        return -1.0


# trueinrow(C < C1, 5) = 5 and H > H1 and X > L1 + ((H1 - L1) / 2) with X = signal threshold
def sell_5h_close_at(data, ticker):
    close1 = data[-2][ticker]["close"]
    close2 = data[-3][ticker]["close"]
    close3 = data[-4][ticker]["close"]
    close4 = data[-5][ticker]["close"]
    close5 = data[-6][ticker]["close"]
    low = data[-1][ticker]["low"]
    low1 = data[-2][ticker]["low"]
    high1 = data[-2][ticker]["high"]
    high = data[-1][ticker]["high"]

    if close1 >= close2 and close1 >= close3 and close1 >= close4 and close1 >= close5 and high > high1:
        threshold = high1 - ((high1 - low1) / 2)
        # return threshold for confirmation if above day low
        if low < threshold:
            return threshold
        else:
            return -1.0
    else:
        return -1.0


# h = maxh5 and X < H1 - ((H1 - L1) / 2) with X = signal threshold
def sell_5h_high_at(data, ticker):
    high = data[-1][ticker]["high"]
    low = data[-1][ticker]["low"]
    high1 = data[-2][ticker]["high"]
    high2 = data[-3][ticker]["high"]
    high3 = data[-4][ticker]["high"]
    high4 = data[-5][ticker]["high"]
    low1 = data[-2][ticker]["low"]

    if high >= high1 and high >= high2 and high >= high3 and high >= high4:
        threshold = high1 - ((high1 - low1) / 2)
        # return threshold for confirmation if above day low
        if low < threshold:
            return threshold
        else:
            return -1.0
    else:
        return -1.0

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["SPY"]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        assets = [];
        for ticker in self.tickers:
            assets.append(ticker);
            # shorting seemingly not supported
        return assets

    def run(self, data):
        allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        d = data["ohlcv"]
        for ticker in self.tickers:
            threshold = buy_5l_close_at(d, ticker);
            if threshold > -1.0:
                if data["holdings"][ticker] >= 0:
                    log("[buy_5l_close_at] buy " + ticker + " at: " + data[-1]["close"] + " (signal threshold: " + threshold + ")");
                    stake = min(1, data["holdings"][ticker]+0.1)
                    log("[buy_5l_close_at] new stake for " + ticker + ": " + stake);
                    continue;
                else:
                    # shorting seemingly not supported
                    continue;
            threshold = buy_5l_low_at(d, ticker);
            if threshold > -1.0:
                if data["holdings"][ticker] >= 0:
                    log("[buy_5l_low_at] buy " + ticker + " at: " + d[-1]["close"] + " (signal threshold: " + threshold + ")");
                    stake = min(1, data["holdings"][ticker]+0.1)
                    log("[buy_5l_low_at] new stake for " + ticker + ": " + stake);
                    continue;
                else:
                    # shorting seemingly not supported
                    continue;

            threshold = sell_5h_close_at(d, ticker);
            if threshold > -1.0:
                if data["holdings"][ticker] > 0:
                    log("[sell_5h_close_at] sell " + ticker + " at: " + data[-1]["close"] + " (signal threshold: " + threshold + ")");
                    stake = min(1, data["holdings"][ticker]-0.1)
                    log("[sell_5h_close_at] new stake for " + ticker + ": " + stake);
                    continue;
                else:
                    # shorting seemingly not supported
                    continue;

            threshold = sell_5h_high_at(d, ticker);
            if threshold > -1.0:
                if data["holdings"][ticker] > 0:
                    log("[sell_5h_high_at] sell " + ticker + " at: " + data[-1]["close"] + " (signal threshold: " + threshold + ")");
                    stake = min(1, data["holdings"][ticker]-0.1)
                    log("[sell_5h_high_at] new stake for " + ticker + ": " + stake);
                    continue;
                else:
                    # shorting seemingly not supported
                    continue;
from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

__author__ = 'Marco Ellwanger'

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
        self.tickers = ["SPY", "NVDA"];

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        assets = [];
        for ticker in self.tickers:
            assets.append(ticker);
            # TODO: figure out shorting
        return assets

    def run(self, data):
        allocation_dict = {};
        d = data["ohlcv"]
        for ticker in self.tickers:
            threshold = buy_5l_close_at(d, ticker);
            if threshold > -1.0:
                if data["holdings"][ticker] >= 0:
                    log("holdings: " + str(data["holdings"][ticker]));
                    log("[buy_5l_close_at] buy " + ticker + " at: " + str(d[-1]["SPY"]["close"]) + " (signal threshold: " + str(threshold) + ")");
                    stake = min(1, data["holdings"][ticker]+0.1);
                    allocation_dict[ticker] = stake;
                    log("[buy_5l_close_at] new stake for " + ticker + ": " + str(stake));
                    continue;
                else:
                    # TODO: figure out shorting
                    continue;

            threshold = buy_5l_low_at(d, ticker);
            if threshold > -1.0:
                if data["holdings"][ticker] >= 0:
                    log("holdings: " + str(data["holdings"][ticker]));
                    log("[buy_5l_low_at] buy " + ticker + " at: " + str(d[-1]["SPY"]["close"]) + " (signal threshold: " + str(threshold) + ")");
                    stake = min(1, data["holdings"][ticker]+0.1);
                    allocation_dict[ticker] = stake;
                    log("[buy_5l_low_at] new stake for " + ticker + ": " + str(stake));
                    continue;
                else:
                    # TODO: figure out shorting
                    continue;

            threshold = sell_5h_close_at(d, ticker);
            if threshold > -1.0:
                if data["holdings"][ticker] > 0:
                    log("[sell_5h_close_at] sell " + ticker + " at: " + str(d[-1]["SPY"]["close"]) + " (signal threshold: " + str(threshold) + ")");
                    stake = min(1, data["holdings"][ticker]-0.1);
                    allocation_dict[ticker] = stake;
                    log("[sell_5h_close_at] new stake for " + ticker + ": " + str(stake));
                    continue;
                else:
                    # TODO: figure out shorting
                    continue;

            threshold = sell_5h_high_at(d, ticker);
            if threshold > -1.0:
                if data["holdings"][ticker] > 0:
                    log("[sell_5h_high_at] sell " + ticker + " at: " + str(d[-1]["SPY"]["close"]) + " (signal threshold: " + str(threshold) + ")");
                    stake = min(1, data["holdings"][ticker]-0.1);
                    allocation_dict[ticker] = stake;
                    log("[sell_5h_high_at] new stake for " + ticker + ": " + str(stake));
                    continue;
                else:
                    # TODO: figure out shorting
                    continue;
        log("returning allocation_dict=" + str(allocation_dict));
        return allocation_dict;
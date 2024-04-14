from surmount.base_class import Strategy, TargetAllocation

class KevinStrategy(Strategy):

    def __init__(self):
        self.tickers = ["SPY", ...]
        self.data_list = [...]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
    allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
    d = data["ohlcv"]
    for ticker, alloc in allocation_dict:
        if buy_5l_close_at(data, ticker):
            if ()

    if buy_5l_close_at(data)
    # WRITE YOUR STRATEGY LOGIC HERE
    return TargetAllocation(allocation_dict)

    def get_5h_signal(index=None):
    if index is None:
        return KevinStrategy.df['5H']
    elif index >= len(KevinStrategy.df):
        return 0
    else:
        return KevinStrategy.df['5H'][index]


    def get_5l_signal(index=None):
        if index is None:
            return KevinStrategy.df['5L']
        elif index >= len(KevinStrategy.df):
            return 0
        else:
            return KevinStrategy.df['5L'][index]


    def get_open(index=None):
        if index is None:
            return KevinStrategy.df.Open
        elif index >= len(KevinStrategy.df):
            return -1
        else:
            return KevinStrategy.df['Open'][index]


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
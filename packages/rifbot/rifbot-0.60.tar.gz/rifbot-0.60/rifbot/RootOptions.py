import json


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class RootOptions:
    def __init__(self):
        # self.__typename = 'RootOptionsInput'
        self.runType = 'backtest'
        self.capitalFloorPercentage = float(0.4)

        # EngineOptions
        self.exchange = {'id': 'none', 'type': 'binance', 'label': 'Binance'}
        self.groupId = ''
        self.symbol = {'asset': 'BTC', 'currency': 'USDT'}
        self.timeFrame = {'minutes': 60, 'label': '1h'}
        self.start = 1547337600000  # '2019-01-13'
        self.end = 1547424000000  # '2019-01-14'
        self.liveOnly = False
        self.initialCapital = 10000
        self.startPaused = False
        self.strategy = {'value': 'turtle', 'label': 'turtle'}
        self.modulo = 10
        # IndicatorsOptions
        self.ATRLength = 10
        self.EMALength = 10
        self.includeCurrentCandlestick = True
        self.enterPeriod = 10
        self.closePeriod = 8
        self.warmUpCandleCount = 0

        # StrategyOptions
        self.pyramiding = 4
        self.NStepUp = 0.5
        self.NStepStop = 3
        self.moneyMgtPercentage = 0.12
        self.hardCapSize = 3 * 0.18
        self.percentEquity = False

    # def toJson(self):
    #     return json.dumps(self, default=lambda o: o.__dict__)

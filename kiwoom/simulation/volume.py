'''
if (장대양봉[yesterday] or 갭상승[yeseterday]) & 거래량 터짐[yesterday] :
    if 거래량[yesterday] > 거래량[today]:
        buy! # 매수세가 강함
    elif 거래량[yesterday] < 거래량[today]:
        sell! # 매도세가 강함
elif (장대음봉[yesterday] or 갭하락[yestreday]) & 거래량 터짐[yesterday] :
    if 거래량[yesterday] < 거래량[today]:
        buy! # 매수세 강함
    elif 거래량[yesterday] > 거래량[today]:
        sell! # 매도세 강함
'''

class VolumeCheck:
    def __init__(self):
        pass

    def CandleStick(self):
        if self.close < self.open:
            print("Bullish Candle") # 음봉
        elif self.close > self.open:
            print("Bearish Candle") # 양봉
        pass

    def LargeVolume(self):
        pass
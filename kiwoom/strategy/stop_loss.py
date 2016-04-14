from kiwoom.strategy.base import StrategyBase


class StopLoss(StrategyBase):
    threshold = -0.03

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        현재가 = int(self.ocx.dynamicCall("GetCommRealData(QString, int)", "주식체결", 10))
        잔고_dic = self.data["잔고_dic"]
        매입가 = 잔고_dic[sJongmokCode][2]
        보유수량 = 잔고_dic[sJongmokCode][3]

        if 보유수량 == 0:
            return

        if (현재가 - 매입가) / 매입가 < self.threshold:
            self.on_sell_signal(sJongmokCode, 보유수량)

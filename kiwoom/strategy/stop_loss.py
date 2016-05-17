from kiwoom.strategy.base import StrategyBase


class StopLoss(StrategyBase):
    threshold = -0.03

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        print("on_real_data", "StopLoss")
        현재가 = self.data.get_balance_current_price(sJongmokCode)
        매입가 = self.data.get_balance_buy_price(sJongmokCode)
        보유수량 = self.data.get_balance_hold_amount(sJongmokCode)

        if 보유수량 == 0:
            return

        if (현재가 - 매입가) / 매입가 < self.threshold:
            self.on_sell_signal(sJongmokCode, 보유수량)
            self.data.set_balance()

            cur_balance_dic = {"매도전략": []}
            self.data.set_balance(sJongmokCode, cur_balance_dic)  # 매도전략 초기화

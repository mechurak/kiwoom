from kiwoom.strategy.base import StrategyBase


class JustBuy(StrategyBase):

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        print("on_real_data", "JustBuy")
        목표보유수량 = self.data.get_balance_target_hold_amount(sJongmokCode)
        보유수량 = self.data.get_balance_hold_amount(sJongmokCode)

        if 목표보유수량 == 0 or 목표보유수량 == 보유수량:
            return
        else:
            self.on_buy_signal(sJongmokCode, 목표보유수량 - 보유수량)
            cur_balance_dic = {"매수전략": []}
            self.data.set_balance(sJongmokCode, cur_balance_dic)  # 매수전략 초기화

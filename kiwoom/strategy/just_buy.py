from kiwoom.strategy.base import StrategyBase


class JustBuy(StrategyBase):

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        print("on_real_data", "JustBuy")
        if self.is_done:
            print("is_done")
            return

        목표보유수량 = self.balance.목표보유수량
        보유수량 = self.balance.보유수량

        if 목표보유수량 == 0 or 목표보유수량 == 보유수량:
            return
        else:
            self.on_buy_signal(목표보유수량 - 보유수량)

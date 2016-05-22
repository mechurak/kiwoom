from kiwoom.strategy.base import StrategyBase


class ConditionSell(StrategyBase):
    threshold = 0.02

    def on_condition(self, condition_index, condition_name):
        print("(on_condition)", condition_index, condition_name)
        if self.is_done:
            print("is_done")
            return

        현재가 = self.balance.현재가
        매입가 = self.balance.매입가
        보유수량 = self.balance.보유수량
        print(현재가, 매입가, 보유수량)

        if 보유수량 == 0:
            return

        if (현재가 - 매입가) / 매입가 > self.threshold:
            self.on_sell_signal(보유수량)

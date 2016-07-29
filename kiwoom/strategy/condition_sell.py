from kiwoom.strategy.base import StrategyBase
from logger import MyLogger


class ConditionSell(StrategyBase):
    threshold = 0.01

    def on_condition(self, condition_index, condition_name):
        MyLogger.instance().logger().info("index: %d, name: %s", condition_index, condition_name)
        if self.is_queued:
            MyLogger.instance().logger().info("is_queued. do nothing")
            return

        if self.balance.보유수량 == 0:
            MyLogger.instance().logger().info("보유수량 == 0. do nothing")
            return

        수익률 = (self.balance.현재가 - self.balance.매입가) / self.balance.매입가
        MyLogger.instance().logger().debug("수익률: %f, 현재가: %d, 매입가: %d, 보유수량: %d", 수익률, self.balance.현재가, self.balance.매입가, self.balance.보유수량)

        if 수익률 > self.threshold:
            MyLogger.instance().logger().info("ConditionSell!!!! 보유수량: %d. 수익률: %f > threshold: %f", self.balance.보유수량, 수익률, self.threshold)
            self.on_sell_signal(self.balance.보유수량)

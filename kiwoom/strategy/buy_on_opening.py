from kiwoom.strategy.base import StrategyBase
from logger import MyLogger


class BuyOnOpening(StrategyBase):

    def on_time(self, cur_time_str):
        MyLogger.instance().logger().info("BuyOnOpening. time: %s. %s", cur_time_str, self.balance.종목명)
        if self.is_queued:
            MyLogger.instance().logger().info("is_queued. do nothing")
            return

        if not self.balance.목표보유수량:
            return

        주문수량 = self.balance.목표보유수량 - self.balance.보유수량

        if self.balance.목표보유수량 == 0 or 주문수량 <= 0:
            MyLogger.instance().logger().info("목표보유수량: %d, 보유수량: %d. do nothing", self.balance.목표보유수량, self.balance.보유수량)
            return

        else:
            MyLogger.instance().logger().info("BuyOnOpening!!!! 주문수량: %d", 주문수량)
            self.on_buy_signal(주문수량)

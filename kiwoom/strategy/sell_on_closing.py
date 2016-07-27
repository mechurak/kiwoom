from kiwoom.strategy.base import StrategyBase
from logger import MyLogger


class SellOnClosing(StrategyBase):

    def on_time(self, cur_time_str):
        MyLogger.instance().logger().info("SellOnClosing. time: %s. %s", cur_time_str, self.balance.종목명)
        if self.is_done:
            MyLogger.instance().logger().info("is_done. do nothing")
            return

        if self.balance.보유수량 > 0:
            MyLogger.instance().logger().info("SellOnClosing!!!! 주문수량: %d", self.balance.보유수량)
            self.on_sell_signal(self.balance.보유수량)

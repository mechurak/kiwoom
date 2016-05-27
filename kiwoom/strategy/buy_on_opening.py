from kiwoom.strategy.base import StrategyBase
from kiwoom.kiwoom import Kiwoom
from logger import MyLogger


class BuyOnOpening(StrategyBase):

    def on_time(self, cur_time_str):
        MyLogger.instance().logger().info("BuyOnOpening %s. %s", cur_time_str, self.balance.종목명)
        kiwoom = Kiwoom.instance()
        kiwoom.tr_code(self.balance.종목코드)

    def on_expect_price(self, expect_price):
        MyLogger.instance().logger().info("BuyOnOpening. expect_price: %d. %s", expect_price, self.balance.종목명)
        if self.is_done:
            MyLogger.instance().logger().info("is_done. do nothing")
            return

        if not self.balance.목표보유수량:
            return

        주문수량 = self.balance.목표보유수량 - self.balance.보유수량

        if self.balance.목표보유수량 == 0 or 주문수량 <= 0:
            MyLogger.instance().logger().info("목표보유수량: %d, 보유수량: %d. do nothing", self.balance.목표보유수량, self.balance.보유수량)
            return

        else:
            MyLogger.instance().logger().info("BuyOnOpening!!!! 주문수량: %d", 주문수량)
            kiwoom = Kiwoom.instance()
            ret = kiwoom.send_order(1, self.balance.종목코드, 주문수량, expect_price, "00")  # 지정가 매수
            if ret == 0:
                self.is_done = True

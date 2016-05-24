from kiwoom.strategy.base import StrategyBase
from logger import MyLogger


class JustBuy(StrategyBase):

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        MyLogger.instance().logger().info("JustBuy")
        if self.is_done:
            MyLogger.instance().logger().info("is_done. do nothing")
            return

        if self.balance.목표보유수량 == 0 or self.balance.목표보유수량 <= self.balance.보유수량:
            MyLogger.instance().logger().info("목표보유수량: %d, 보유수량: %d. do nothing", self.balance.목표보유수량, self.balance.보유수량)
            return
        else:
            MyLogger.instance().logger().info("JustBuy!!!! 주문수량: %d", self.balance.목표보유수량 - self.balance.보유수량)
            self.on_buy_signal(self.balance.목표보유수량 - self.balance.보유수량)

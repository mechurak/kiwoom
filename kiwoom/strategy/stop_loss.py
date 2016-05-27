from kiwoom.strategy.base import StrategyBase
from logger import MyLogger


class StopLoss(StrategyBase):
    threshold = -0.03

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        MyLogger.instance().logger().info("StopLoss. %s", self.balance.종목명)
        if self.is_done:
            MyLogger.instance().logger().info("is_done. do nothing")
            return

        if self.balance.보유수량 == 0:
            MyLogger.instance().logger().info("보유수량 == 0. do nothing")
            return

        수익률 = (self.balance.현재가 - self.balance.매입가) / self.balance.매입가
        MyLogger.instance().logger().debug("수익률: %f, 현재가: %d, 매입가: %d, 보유수량: %d", 수익률, self.balance.현재가, self.balance.매입가, self.balance.보유수량)

        if 수익률 < self.threshold:
            MyLogger.instance().logger().info("StopLoss!!!! 보유수량: %d. 수익률: %f < threshold: %f", self.balance.보유수량, 수익률, self.threshold)
            self.on_sell_signal(self.balance.보유수량)

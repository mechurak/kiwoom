from kiwoom.strategy.base import StrategyBase
from logger import MyLogger


class StopLoss(StrategyBase):
    threshold = -0.03

    def __init__(self, the_balance, the_param_dic):
        super().__init__(the_balance, the_param_dic)
        MyLogger.instance().logger().debug("StopLoss. %s, %s", the_balance, str(the_param_dic))
        if 'threshold' in the_param_dic:
            self.threshold = the_param_dic['threshold']

    @staticmethod
    def get_default_param():
        return {"threshold": -0.03}

    def get_current_param(self):
        return {"threshold": self.threshold}

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        MyLogger.instance().logger().info("StopLoss. %s", self.balance.종목명)
        if self.is_queued:
            MyLogger.instance().logger().info("is_queued. do nothing")
            return

        if self.balance.보유수량 == 0:
            MyLogger.instance().logger().info("보유수량 == 0. do nothing")
            return

        수익률 = self.balance.get_return_rate()
        MyLogger.instance().logger().debug("종목명: %s, 수익률: %f, 현재가: %d, 매입가: %d, 보유수량: %d", self.balance.종목명, 수익률, self.balance.현재가, self.balance.매입가, self.balance.보유수량)

        if 수익률 < self.threshold:
            MyLogger.instance().logger().info("StopLoss!!!! 종목명: %s, 보유수량: %d. 수익률: %f < threshold: %f", self.balance.종목명, self.balance.보유수량, 수익률, self.threshold)
            self.on_sell_signal(self.balance.보유수량)

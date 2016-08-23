from kiwoom.strategy.base import StrategyBase
from logger import MyLogger


class ConditionSell(StrategyBase):
    threshold = 0.01  # 1% 이상 수익이 아니라면 팔지 않음

    def __init__(self, the_balance, the_param_dic):
        super().__init__(the_balance, the_param_dic)
        MyLogger.instance().logger().debug("ConditionSell. %s, %s", the_balance, str(the_param_dic))
        if 'threshold' in the_param_dic:
            self.threshold = the_param_dic['threshold']

    @staticmethod
    def get_default_param():
        return {"threshold": 0.01}

    def get_current_param(self):
        return {"threshold": self.threshold}

    def on_condition(self, condition_index, condition_name):
        MyLogger.instance().logger().info("index: %d, name: %s", condition_index, condition_name)
        if self.is_queued:
            MyLogger.instance().logger().info("is_queued. do nothing")
            return

        if self.balance.보유수량 == 0:
            MyLogger.instance().logger().info("보유수량 == 0. do nothing")
            return

        수익률 = self.balance.get_return_rate()
        MyLogger.instance().logger().debug("종목명: %s, 수익률: %f, 현재가: %d, 매입가: %d, 보유수량: %d", self.balance.종목명, 수익률, self.balance.현재가, self.balance.매입가, self.balance.보유수량)

        if 수익률 > self.threshold:
            MyLogger.instance().logger().info("ConditionSell!!!! %s 종목명: %s, 보유수량: %d. 수익률: %f > threshold: %f", condition_name, self.balance.종목명, self.balance.보유수량, 수익률, self.threshold)
            self.on_sell_signal(self.balance.보유수량)

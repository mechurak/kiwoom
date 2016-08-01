from kiwoom.strategy.base import StrategyBase
from logger import MyLogger


class BuyOnOpening(StrategyBase):
    budget = 30  # 만원

    def __init__(self, the_balance, the_param_dic):
        super().__init__(the_balance, the_param_dic)
        MyLogger.instance().logger().debug("BuyOnOpening. %s, %s", the_balance, str(the_param_dic))
        if 'budget' in the_param_dic:
            self.budget = the_param_dic['budget']

    @staticmethod
    def get_default_param():
        return {"budget": 30}

    def get_current_param(self):
        return {"budget": self.budget}

    def on_tr_data(self, current_price):
        # TODO 동시호가때 너무 올랐을 경우 대비 필요함 (현재가에 몇 프로 더해서 계산?)
        self.balance.목표보유수량 = (self.budget * 10000) // self.balance.현재가
        MyLogger.instance().logger().info("예산: %d만원, 목표보유수량: %d", self.budget, self.balance.목표보유수량)

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

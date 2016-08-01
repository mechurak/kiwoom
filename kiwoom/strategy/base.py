from logger import MyLogger
from kiwoom.kiwoom import Kiwoom
from kiwoom.kiwoom import Job


class StrategyBase:
    is_queued = False
    balance = None

    def __init__(self, the_balance, the_param_dic):
        MyLogger.instance().logger().debug("StrategyBase. %s, %s", the_balance, str(the_param_dic))
        self.balance = the_balance

    @staticmethod
    def get_default_param():
        return {}

    def get_current_param(self):
        return {}

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        pass

    def on_condition(self, condition_index, condition_name):
        pass

    def on_time(self, cur_time_str):
        pass

    def on_tr_data(self, current_price):
        pass

    def on_buy_signal(self, 주문수량):
        MyLogger.instance().logger().info("종목명: %s, 주문수량: %d", self.balance.종목명, 주문수량)
        kiwoom = Kiwoom.instance()
        job = Job(kiwoom.send_order, 1, self.balance.종목코드, 주문수량, 0, "03")  # 시장가로 매수
        kiwoom.job_queue.put(job)
        self.is_queued = True
        # TODO 실제 주문 (키움 API) 리턴 값이 0 인지 확인은 안해도 괜찮을까

    def on_sell_signal(self, 주문수량):
        MyLogger.instance().logger().info("종목명: %s, 주문수량: %d", self.balance.종목명, 주문수량)
        kiwoom = Kiwoom.instance()
        job = Job(kiwoom.send_order, 2, self.balance.종목코드, 주문수량, 0, "03")  # 시장가로 매도
        kiwoom.job_queue.put(job)
        self.is_queued = True


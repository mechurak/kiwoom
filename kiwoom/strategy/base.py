from kiwoom.data import Balance
from kiwoom.kiwoom import Kiwoom


class StrategyBase:
    is_done = False
    balance = None

    def __init__(self, the_balance):
        self.balance = the_balance
        print("StrategyBase", self.balance.종목명)

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        pass

    def on_buy_signal(self, 주문수량):
        print("(on_buy_signal)", 주문수량)
        kiwoom = Kiwoom.instance()
        ret = kiwoom.send_order(1, self.balance.종목코드, 주문수량, 0, "03")  # 시장가로 매수
        if ret == 0:
            self.is_done = True

    def on_sell_signal(self, 주문수량):
        print("(on_sell_signal)", 주문수량)
        kiwoom = Kiwoom.instance()
        ret = kiwoom.send_order(2, self.balance.종목코드, 주문수량, 0, "03")  # 시장가로 매도
        if ret == 0:
            self.is_done = True

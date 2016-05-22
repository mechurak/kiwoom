class Balance:
    종목코드 = "000000"
    종목명 = "종목명1"
    현재가 = 15000
    매입가 = None
    보유수량 = 0
    목표보유수량 = None
    수익률 = None
    매수전략 = None
    매도전략 = None

    def __init__(self, the_종목코드):
        self.종목코드 = the_종목코드
        self.매수전략 = {}
        self.매도전략 = {}

    @staticmethod
    def get_table_header():
        return ["종목코드", "종목명", "현재가", "매입가", "보유수량", "목표보유수량", "수익률", "매수전략", "매도전략"]

    @staticmethod
    def get_available_buy_strategy():
        return ["buy_just_buy"]

    @staticmethod
    def get_available_sell_strategy():
        return ["sell_stop_loss", "sell_condition_sell"]

    def get_str_list(self):
        return [self.종목코드, self.종목명, str(self.현재가), str(self.매입가), str(self.보유수량), str(self.목표보유수량), str(self.수익률), str(list(self.매수전략.keys())), str(list(self.매도전략.keys()))]

    def print(self):
        print("\t", self.get_str_list())

    def add_buy_strategy(self, the_전략명):
        from kiwoom.strategy.just_buy import JustBuy
        if the_전략명 not in self.매수전략:
            if the_전략명 == "buy_just_buy":
                buy_just_buy = JustBuy(self)
                self.매수전략[the_전략명] = buy_just_buy
                print("add_buy_strategy. buy_just_buy 추가됨.", self.종목명)
            elif the_전략명 == "next_strategy":
                print("add_sell_strategy. unknown strategy")
                pass
            else:
                print("add_sell_strategy. unknown strategy")

    def add_sell_strategy(self, the_전략명):
        from kiwoom.strategy.stop_loss import StopLoss
        from kiwoom.strategy.condition_sell import ConditionSell
        if the_전략명 not in self.매도전략:
            if the_전략명 == "sell_stop_loss":
                sell_stop_loss = StopLoss(self)
                self.매도전략[the_전략명] = sell_stop_loss
                print("add_sell_strategy. sell_stop_loss 추가됨.", self.종목명)
            elif the_전략명 == "sell_condition_sell":
                sell_condition_sell = ConditionSell(self)
                self.매도전략[the_전략명] = sell_condition_sell
                print("add_sell_strategy. sell_condition_sell 추가됨.", self.종목명)
                pass
            else:
                print("add_sell_strategy. unknown strategy")

    def remove_buy_strategy(self, the_전략명):
        if the_전략명 not in self.매수전략:
            del self.매수전략[the_전략명]

    def remove_sell_strategy(self, the_전략명):
        if the_전략명 not in self.매도전략:
            del self.매도전략[the_전략명]


class Condition:
    인덱스 = -1
    조건명 = "temp"
    신호종류 = "미지정"   # "매도신호", "매수신호", "미지정"
    적용유무 = "0"        # "0": 실시간 등록은 하지 않음, "1": 실시간 등록 예정

    def __init__(self, the_인덱스):
        self.인덱스 = the_인덱스

    @staticmethod
    def get_table_header():
        return ["인덱스", "조건명", "신호종류", "적용유무", "요청버튼"]

    @staticmethod
    def get_signal_type_items_list():
        return ["매도신호", "매수신호", "미지정"]

    @staticmethod
    def get_applied_items_list():
        return ["0", "1"]

    def print(self):
        print("\t", self.인덱스, self.조건명, self.신호종류, self.적용유무)


class Data:
    계좌번호 = "12345"
    계좌번호_list = ["12345", "23456"]
    조건식_dic = {}  # {0: Condition(0), 1: Condition(1)}
    잔고_dic = {}  # {"00000": Balance("00000"), "00001": Balance("00001")}

    def print(self):
        print("계좌번호", self.계좌번호)
        print("계좌번호_list", self.계좌번호_list)
        print("조건식_dic ==============")
        for condition in self.조건식_dic.values():
            condition.print()
        print("잔고_dic ==============")
        for balance in self.잔고_dic.values():
            balance.print()

    def get_condition(self, the_인덱스):
        if the_인덱스 not in self.조건식_dic:
            self.조건식_dic[the_인덱스] = Condition(the_인덱스)
        return self.조건식_dic[the_인덱스]

    def get_balance(self, the_종목코드):
        if the_종목코드 not in self.잔고_dic:
            self.잔고_dic[the_종목코드] = Balance(the_종목코드)
        return self.잔고_dic[the_종목코드]

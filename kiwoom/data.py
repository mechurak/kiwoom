class Balance:
    종목코드 = "000000"
    종목명 = "종목명1"
    현재가 = 15000
    매입가 = None
    보유수량 = 0
    목표보유수량 = None
    수익률 = None
    매수전략 = []
    매도전략 = []

    def __init__(self, the_종목코드):
        self.종목코드 = the_종목코드

    def update(self, the_잔고_dic):
        if "종목명" in the_잔고_dic:
            self.종목명 = the_잔고_dic["종목명"]
        if "현재가" in the_잔고_dic:
            self.현재가 = the_잔고_dic["현재가"]
            self.현재가 = int(self.현재가)
        if "매입가" in the_잔고_dic:
            self.매입가 = the_잔고_dic["매입가"]
            self.매입가 = int(self.매입가)
        if "보유수량" in the_잔고_dic:
            self.보유수량 = the_잔고_dic["보유수량"]
            self.보유수량 = int(self.보유수량)
        if "목표보유수량" in the_잔고_dic:
            self.목표보유수량 = the_잔고_dic["목표보유수량"]
            self.목표보유수량 = int(self.목표보유수량)
        if "수익률" in the_잔고_dic:
            self.수익률 = the_잔고_dic["수익률"]
            self.수익률 = float(self.수익률)
        if "매수전략" in the_잔고_dic:
            self.매수전략 = the_잔고_dic["매수전략"]
        if "매도전략" in the_잔고_dic:
            self.매도전략 = the_잔고_dic["매도전략"]


class Data:
    조건식_list = [[0, "조건식0", "매도신호", "0"]]
    계좌번호 = "12345"
    계좌번호_list = ["12345", "23456"]
    잔고_dic = {}
    #잔고_dic = {"00000": Balance("00000"), "00001": Balance("00001")}
    매수전략_dic = {}
    매도전략_dic = {}

    def print(self):
        print("계좌번호", self.계좌번호)
        print("계좌번호_list", self.계좌번호_list)
        print("조건식_list", self.조건식_list)
        print("잔고_dic", self.get_balance_list())
        print("매수전략_list", self.매수전략_dic)
        print("매도전략_list", self.매도전략_dic)

    def get_condition_header(self):
        return ["인덱스", "조건명", "신호종류", "적용유무", "요청버튼"]

    def get_balance_header(self):
        return ["종목코드", "종목명", "현재가", "매입가", "보유수량", "목표보유수량", "수익률", "매수전략", "매도전략"]

    def get_balance_list(self):
        ret = []
        for balance in self.잔고_dic.values():
            ret.append([balance.종목코드, balance.종목명, balance.현재가, balance.매입가, balance.보유수량, balance.목표보유수량, balance.수익률, balance.매수전략, balance.매도전략])
        return ret

    def set_balance(self, the_종목코드, the_잔고_dic):
        if the_종목코드 not in self.잔고_dic:
            self.잔고_dic[the_종목코드] = Balance(the_종목코드)

        balance = self.잔고_dic[the_종목코드]
        balance.update(the_잔고_dic)

    def get_balance_hold_amount(self, the_종목코드):
        if the_종목코드 not in self.잔고_dic:
            return 0
        balance = self.잔고_dic[the_종목코드]
        return balance.보유수량

    def get_balance_target_hold_amount(self, the_종목코드):
        if the_종목코드 not in self.잔고_dic:
            return 0
        balance = self.잔고_dic[the_종목코드]
        return balance.목표보유수량

    def get_balance_current_price(self, the_종목코드):
        if the_종목코드 not in self.잔고_dic:
            return 0
        balance = self.잔고_dic[the_종목코드]
        return balance.현재가

    def get_balance_buy_price(self, the_종목코드):
        if the_종목코드 not in self.잔고_dic:
            return 0
        balance = self.잔고_dic[the_종목코드]
        return balance.매입가

    def get_balance_buy_strategy(self, the_종목코드):
        if the_종목코드 not in self.잔고_dic:
            return []
        매수전략_list = self.잔고_dic[the_종목코드].매수전략
        ret = []
        for 매수전략_str in 매수전략_list:
            ret.append(self.매수전략_dic[매수전략_str])
        return ret

    def get_balance_sell_strategy(self, the_종목코드):
        if the_종목코드 not in self.잔고_dic:
            return []
        매도전략_list = self.잔고_dic[the_종목코드].매도전략
        ret = []
        for 매도전략_str in 매도전략_list:
            ret.append(self.매도전략_dic[매도전략_str])
        return ret
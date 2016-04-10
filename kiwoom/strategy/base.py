class StrategyBase:
    def __init__(self, ocx, data):
        self.ocx = ocx
        self.data = data

    def on_real_data(self, sJongmokCode, sRealType, sRealData):
        pass

    def on_buy_signal(self, 종목코드, 주문수량):
        print("(on_buy_signal)", 종목코드, 주문수량)

    def on_sell_signal(self, 종목코드, 주문수량):
        print("(on_sell_signal)", 종목코드, 주문수량)
        self.send_order(2, 종목코드, 주문수량, 0, "03")  # 시장가로 매도

    def send_order(self, 주문유형, 종목코드, 주문수량, 주문단가, 거래구분):
        print("(send_order)", 주문유형, 종목코드, 주문수량, 주문단가, 거래구분)
        sRQName = "주식주문"
        sScreenNo = "1111"
        ret = self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                   [sRQName, sScreenNo, self.data["계좌번호"], 주문유형, 종목코드, 주문수량, 주문단가, 거래구분, ""])
        print(ret)


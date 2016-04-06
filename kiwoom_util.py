class KiwoomUtil:
    def __init__(self, ocx, my_data):
        self.ocx = ocx
        self.my_data = my_data

    def login(self):
        if self.ocx.dynamicCall("GetConnectState()") == 0:
            self.ocx.dynamicCall("CommConnect()")

    def refresh_condition_dic(self):
        success = self.ocx.dynamicCall("GetConditionLoad()")
        print(success)

    def tr_condition_result(self, condition):
        ret = self.ocx.dynamicCall("SendCondition(QString, QString, int, int)", "0101", condition[1], condition[0], 0)
        print("SendCondition ret: ", ret)

    def tr_balance(self):
        계좌번호 = self.my_data["계좌번호"]
        print("계좌번호", 계좌번호)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "계좌번호", 계좌번호)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "조회구분", 2)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", 0, "0101")

    def tr_code(self, 종목코드):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", 종목코드)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", 0, "0102")

    def set_real_reg(self, 종목코드_list_str):
        screenNum = "0103"
        fid = "9001;10;13;21;41"
        ret = self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", [screenNum, 종목코드_list_str, fid, "0"])
        print("ret ", ret)



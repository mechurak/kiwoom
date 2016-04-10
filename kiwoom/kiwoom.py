from PyQt4.QAxContainer import *
from PyQt4.QtCore import *


class Kiwoom:
    data = {
            "조건식_list_header": ["인덱스", "조건명", "신호종류", "적용유무"],
            "조건식_list": [[0, "조건식0", "매도신호", False]],
            "계좌번호": "12345",
            "잔고_dic_header": ["종목명", "현재가", "매앱가", "수익율", "매수전략", "매도전략"],
            "잔고_dic": {"00000": ["종목명1", 15000, 10000, 0.5, False, False],
                       "00001": ["종목명2", 15000, 10000, 0.5, False, False]
                       },
            }

    def __init__(self, the_callback):
        self.callback = the_callback

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveRealData(QString, QString, QString)"), self.OnReceiveRealData)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"), self.OnReceiveMsg)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveChejanData(QString, int, QString)"), self.OnReceiveChejanData)
        self.ocx.connect(self.ocx, SIGNAL("OnEventConnect(int)"), self.OnEventConnect)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveCondition(QString, QString, QString, QString)"), self.OnReceiveCondition)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveTrCondition(QString, QString, QString, int, int)"), self.OnReceiveTrCondition)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveConditionVer(int, QString)"), self.OnReceiveConditionVer)

        self.login()

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        print("(OnReceiveTrData) ", sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg)
        if sRQName == "주식기본정보요청":
            name = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "종목명")
            volume = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "거래량")
            retStr = ""
            retStr += "종목명: " + name.strip() + "\n"
            retStr += "거래량: " + volume.strip() + "\n"
            self.callback.on_print(retStr)

        elif sRQName == "계좌평가잔고내역요청":
            print("계좌평가잔고내역요청")
            count = self.ocx.dynamicCall("GetDataCount(QString)", ["계좌평가잔고개별합산"])
            print("count: ", count)
            잔고_dic = self.data["잔고_dic"]
            잔고_dic.clear()
            for i in range(0, count):
                code = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "종목번호")
                name = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "종목명")
                cur_price = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "현재가")
                buy_price = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "매입가")
                earnings_rate = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "수익률(%)")
                code = code.strip()
                name = name.strip()
                cur_price = int(cur_price.strip())
                buy_price = int(buy_price.strip())
                earnings_rate = float(earnings_rate.strip())
                earnings_rate /= 100
                print("수익률", earnings_rate)
                print(name, "현재가: ", cur_price, "매입가: ", buy_price, "수익률: ", earnings_rate)
                잔고_dic[code] = [name, cur_price, buy_price, earnings_rate, True, True]
            self.callback.on_data_updated(["잔고_dic"])

    def OnReceiveRealData(self, sJongmokCode, sRealType, sRealData):
        print("(OnReceiveRealData) ", sJongmokCode, ", ", sRealType, ", ", sRealData)
        잔고_dic = self.data["잔고_dic"]
        if sJongmokCode in 잔고_dic:
            매수전략_list = 잔고_dic[sJongmokCode]["매수전략"]
            for 매수전략 in 매수전략_list:
                매수전략.onRealData(sJongmokCode, sRealType, sRealData)

            매도전략_list = 잔고_dic[sJongmokCode]["매도전략"]
            for 매도전략 in 매도전략_list:
                매도전략.onRealData(sJongmokCode, sRealType, sRealData)

    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        print("(OnReceiveMsg) ", sScrNo, sRQName, sTrCode, sMsg)

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        print("(OnReceiveChejanData) ", sGubun, nItemCnt, sFidList)

    def OnEventConnect(self, nErrCode):
        if nErrCode == 0:
            print("로그인 성공")
            self.callback.on_print("로그인 성공")
            account_num = self.ocx.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
            account_num = account_num[:-1]
            account_list = account_num.split(";")
            self.data["계좌번호"] = account_list[0]
            self.callback.on_data_updated(["계좌번호"])
            self.callback.on_connected()

    def OnReceiveCondition(self, strCode, strType, strConditionName, strConditionIndex):
        print("(OnReceiveCondition) ", strCode, strType, strConditionName, strConditionIndex)

    def OnReceiveTrCondition(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        print("(OnReceiveTrCondition) ", sScrNo, strCodeList, strConditionName, nIndex, nNext)
        code_list_str = strCodeList[:-1]  # 마지막 ";" 제거
        code_list = code_list_str.split(';')
        print(code_list)
        for code in code_list:
            name = self.ocx.dynamicCall("GetMasterCodeName(QString)", [code])
            print(name)

    def OnReceiveConditionVer(self, lRet, sMsg):
        print("(OnReceiveConditionVer) ", lRet, sMsg)
        condition_ret = self.ocx.dynamicCall("GetConditionNameList()")
        condition_ret = condition_ret[:-1]  # 마지막 ";" 제거
        print(condition_ret)
        condition_list_raw = condition_ret.split(";")
        print(condition_list_raw)
        condition_list = self.data["조건식_list"]
        condition_list.clear()
        for condition_with_index in condition_list_raw:
            if condition_with_index == "":
                continue
            cur = condition_with_index.split("^")
            cur_list = [int(cur[0]), cur[1], "미지정", False]
            condition_list.append(cur_list)
        print(condition_list)
        self.callback.on_data_updated(["조건식_list"])

    ##############################################################
    # Functions
    ##############################################################

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
        account = self.data["계좌번호"]
        print("계좌번호", account)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "조회구분", 2)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", 0, "0101")

    def tr_code(self, 종목코드):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", 종목코드)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", 0, "0102")

    def set_real_reg(self, 종목코드_list_str):
        screen_num = "0103"
        fid = "9001;10;13;21;41"
        ret = self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", [screen_num, 종목코드_list_str, fid, "0"])
        print("ret ", ret)


class KiwoomCallback:
    def on_connected(self):
        pass

    def on_data_updated(self, key_list):
        pass

    def on_print(self, log_str):
        pass




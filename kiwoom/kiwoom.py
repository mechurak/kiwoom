from PyQt4.QAxContainer import *
from PyQt4.QtCore import *
from kiwoom.strategy.stop_loss import StopLoss
from kiwoom.strategy.just_buy import JustBuy
from kiwoom.data import Data
from kiwoom import constant


class Kiwoom:
    data = Data()

    def __init__(self, the_callback):
        self.callback = the_callback

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveRealData(QString, QString, QString)"), self.OnReceiveRealData)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveRealCondition(QString, QString, QString, QString)"), self.OnReceiveRealCondition)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"), self.OnReceiveMsg)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveChejanData(QString, int, QString)"), self.OnReceiveChejanData)
        self.ocx.connect(self.ocx, SIGNAL("OnEventConnect(int)"), self.OnEventConnect)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveCondition(QString, QString, QString, QString)"), self.OnReceiveCondition)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveTrCondition(QString, QString, QString, int, int)"), self.OnReceiveTrCondition)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveConditionVer(int, QString)"), self.OnReceiveConditionVer)

        sell_stop_loss = StopLoss(self.ocx, self.data)
        self.data.매도전략_dic["sell_stop_loss"] = sell_stop_loss

        buy_just_buy = JustBuy(self.ocx, self.data)
        self.data.매수전략_dic["buy_just_buy"] = buy_just_buy

        self.login()

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        print("(OnReceiveTrData) ", sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg)
        if sRQName == "주식기본정보요청":
            종목코드 = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "종목코드")
            종목명 = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "종목명")
            현재가_str = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "현재가")
            종목코드 = 종목코드.strip()
            종목명 = 종목명.strip()
            현재가_str = 현재가_str.strip()

            if 종목코드 and 종목명 and 현재가_str:
                print(종목코드, 종목명, 현재가_str)
                종목코드 = 종목코드.strip()
                종목명 = 종목명.strip()
                현재가 = int(현재가_str.strip())

                cur_balance_dic = {"종목명": 종목명, "현재가": 현재가}
                self.data.set_balance(종목코드, cur_balance_dic)
                self.callback.on_data_updated(["잔고_dic"])
            else:
                print("잘못된 종목 코드")

        elif sRQName == "계좌평가잔고내역요청":
            print("계좌평가잔고내역요청")
            count = self.ocx.dynamicCall("GetDataCount(QString)", ["계좌평가잔고개별합산"])
            print("count: ", count)
            for i in range(0, count):
                종목번호 = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "종목번호")
                종목명 = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "종목명")
                현재가_str = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "현재가")
                매입가_str = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "매입가")
                보유수량_str = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "보유수량")
                수익률_str = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "수익률(%)")
                종목번호 = 종목번호.strip()
                종목코드 = 종목번호[1:]  # 앞에 'A' 제거
                종목명 = 종목명.strip()
                현재가 = int(현재가_str.strip())
                매입가 = int(매입가_str.strip())
                보유수량 = int(보유수량_str.strip())
                수익률 = float(수익률_str.strip()) / 100
                print("수익률", 수익률)
                print(종목명, "현재가: ", 현재가, "매입가: ", 매입가, "보유수량: ", 보유수량, "수익률: ", 수익률)
                cur_balance_dic = {"종목명": 종목명, "현재가": 현재가, "매입가": 매입가, "보유수량": 보유수량, "수익률": 수익률}
                self.data.set_balance(종목코드, cur_balance_dic)

            self.callback.on_data_updated(["잔고_dic"])

    def OnReceiveRealData(self, sJongmokCode, sRealType, sRealData):
        print("(OnReceiveRealData) ", sJongmokCode, ", ", sRealType, ", ", sRealData)
        if sJongmokCode in self.data.잔고_dic:
            if (sRealType == "주식체결"):
                현재가_str = self.ocx.dynamicCall("GetCommRealData(QString, int)", "주식체결", 10)
                현재가 = int(현재가_str.strip())
                cur_balance_dic = {"현재가": 현재가}
                self.data.set_balance(sJongmokCode, cur_balance_dic)

                매수전략_list = self.data.get_balance_buy_strategy(sJongmokCode)
                for 매수전략 in 매수전략_list:
                    매수전략.on_real_data(sJongmokCode, sRealType, sRealData)

                매도전략_list = self.data.get_balance_sell_strategy(sJongmokCode)
                for 매도전략 in 매도전략_list:
                    매도전략.on_real_data(sJongmokCode, sRealType, sRealData)

    def OnReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        print("(OnReceiveRealCondition)", strCode, strType, strConditionName, strConditionIndex)
        if strType == 'I':  # 조건식 편입
            if self.data.get_condition_signal_type(strConditionIndex) == "매도신호":
                보유수량 = self.data.get_balance_hold_amount(strCode)
                if 보유수량 > 0:
                    self.send_order(2, strCode, 보유수량, 0, "03")  # 시장가로 매도

        elif strType == 'D':  # 조건식 이탈
            pass

    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        print("(OnReceiveMsg) ", sScrNo, sRQName, sTrCode, sMsg)

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        print("(OnReceiveChejanData) ", sGubun, nItemCnt, sFidList)
        if sGubun == 0:  # 주문체결통보
            pass

        elif sGubun == 1:  # 잔고통보
            종목코드 = self.ocx.dynamicCall("GetChejanData(int)", 9001)
            종목명 = self.ocx.dynamicCall("GetChejanData(int)", 302)
            현재가_str = self.ocx.dynamicCall("GetChejanData(int)", 10)
            보유수량_str = self.ocx.dynamicCall("GetChejanData(int)", 930)
            매입단가_str = self.ocx.dynamicCall("GetChejanData(int)", 931)
            종목코드 = 종목코드.strip()
            종목명 = 종목명.strip()
            현재가 = int(현재가_str.strip())
            매입단가 = int(매입단가_str.strip())
            보유수량 = int(보유수량_str.strip())
            잔고_dic = self.data.잔고_dic

            prev_보유수량 = self.data.get_balance_hold_amount(종목코드)
            if 보유수량 == 0 and prev_보유수량 != 0:  # 해당 종목 청산
                del 잔고_dic[종목코드]
                self.set_real_remove(종목코드)  # 실시간 해제

            elif 보유수량 != 0 and prev_보유수량 == 0:  # 새로운 종목 매수
                cur_balance_dic = {"현재가": 현재가, "매입가": 매입단가, "보유수량": 보유수량}
                self.data.set_balance(종목코드, cur_balance_dic)
                self.set_real_reg([종목코드])  # 실시간 등록

            else:
                print("unexpected condition")

        elif sGubun == 3:  # 특이신호
            pass

    def OnEventConnect(self, nErrCode):
        if nErrCode == 0:
            print("로그인 성공")
            self.callback.on_print("로그인 성공")
            account_num = self.ocx.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
            account_num = account_num[:-1]
            account_list = account_num.split(";")
            self.data.계좌번호_list = account_list
            self.data.계좌번호 = account_list[0]
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
        self.data.조건식_dic.clear()
        for condition_with_index in condition_list_raw:
            if condition_with_index == "":
                continue
            cur = condition_with_index.split("^")
            인덱스 = int(cur[0])
            조건명 = cur[1]
            cur_condition_dic = {"조건명": 조건명}
            self.data.set_condition(인덱스, cur_condition_dic)
        self.callback.on_data_updated(["조건식_dic"])

    ##############################################################
    # Functions
    ##############################################################

    def login(self):
        if self.ocx.dynamicCall("GetConnectState()") == 0:
            self.ocx.dynamicCall("CommConnect()")

    def refresh_condition_dic(self):
        success = self.ocx.dynamicCall("GetConditionLoad()")
        print(success)

    def tr_condition_result(self, 조건명, 인덱스, 신호종류, 적용유무):
        screen_num = constant.SN_조건식_미지정
        if 신호종류 == "매수신호":
            screen_num = constant.SN_조건식_매수신호
        elif 신호종류 == "매도신호":
            screen_num = constant.SN_조건식_매도신호
        print("tr_condition_result", screen_num, 조건명, 인덱스, int(적용유무))
        ret = self.ocx.dynamicCall("SendCondition(QString, QString, int, int)", screen_num, 조건명, 인덱스, int(적용유무))
        print("SendCondition ret: ", ret)

    def tr_balance(self):
        account = self.data.계좌번호
        print("계좌번호", account)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "조회구분", 2)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", 0, constant.SN_잔고조회)

    def tr_code(self, 종목코드):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", 종목코드)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", 0, constant.SN_종목정보)

    def set_real_reg(self, 종목코드_list_str):
        fid = "9001;10;13"  # 종목코드,업종코드;현재가;누적거래량
        ret = self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                                   [constant.SN_실시간조회, 종목코드_list_str, fid, "1"])
        print("SetRealReg. ret ", ret)

    def set_real_remove(self, 종목코드):
        ret = self.ocx.dynamicCall("SetRealRemove(QString, QString)", [constant.SN_실시간조회, 종목코드])
        print("SetRealRemove ret ", ret)

    def send_order(self, 주문유형, 종목코드, 주문수량, 주문단가, 거래구분):
        print("(send_order)", 주문유형, 종목코드, 주문수량, 주문단가, 거래구분)
        sRQName = "주식주문"
        sScreenNo = constant.SN_주식주문
        ret = self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                   [sRQName, sScreenNo, self.data.계좌번호, 주문유형, 종목코드, 주문수량, 주문단가, 거래구분, ""])
        print("send_order. ret", ret)


class KiwoomCallback:
    def on_connected(self):
        pass

    def on_data_updated(self, key_list):
        pass

    def on_print(self, log_str):
        pass

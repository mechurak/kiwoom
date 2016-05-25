from PyQt4.QAxContainer import *
from PyQt4.QtCore import *
from kiwoom.data import Data
from kiwoom import constant
from logger import MyLogger


class Singleton:
    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__get_instance
        return cls.__instance


class Kiwoom(Singleton):
    data = Data()
    callback = None

    def __init__(self):
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
        self.login()

    def set_callback(self, the_callback):
        self.callback = the_callback

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        MyLogger.instance().logger().info("%s, %s, %s, %s, %s, %d, %s, %s, %s", sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg)
        if sRQName == "주식기본정보요청":
            MyLogger.instance().logger().info("sRQName: 계좌평가잔고내역요청")
            종목코드 = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "종목코드")
            종목명 = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "종목명")
            현재가_str = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "현재가")
            종목코드 = 종목코드.strip()
            종목명 = 종목명.strip()
            현재가_str = 현재가_str.strip()

            if 종목코드 and 종목명 and 현재가_str:
                MyLogger.instance().logger().info("종목코드: %s, 종목명: %s, 현재가_str: %s", 종목코드, 종목명, 현재가_str)
                종목코드 = 종목코드.strip()
                종목명 = 종목명.strip()
                현재가 = int(현재가_str.strip())
                if 현재가 < 0:
                    현재가 = 현재가 * (-1)  # 현재가가 음수로 오는 경우가 있음

                balance = self.data.get_balance(종목코드)
                balance.종목명 = 종목명
                balance.현재가 = 현재가
                self.callback.on_data_updated(["잔고_dic"])
            else:
                MyLogger.instance().logger().info("잘못된 종목 코드")

        elif sRQName == "계좌평가잔고내역요청":
            MyLogger.instance().logger().info("sRQName: 계좌평가잔고내역요청")
            count = self.ocx.dynamicCall("GetDataCount(QString)", ["계좌평가잔고개별합산"])
            MyLogger.instance().logger().debug("count: %d", count)
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
                MyLogger.instance().logger().debug("종목명: %s, 현재가: %d, 매입가:%d, 보유수량: %d, 수익률: %f", 종목명, 현재가, 매입가, 보유수량, 수익률)
                balance = self.data.get_balance(종목코드)
                balance.종목명 = 종목명
                balance.현재가 = 현재가
                balance.매입가 = 매입가
                balance.보유수량 = 보유수량
                balance.수익률 = 수익률

            self.callback.on_data_updated(["잔고_dic"])

    def OnReceiveRealData(self, sJongmokCode, sRealType, sRealData):
        MyLogger.instance().logger().info("%s, %s, %s", sJongmokCode, sRealType, sRealData)
        if sJongmokCode in self.data.잔고_dic:
            if (sRealType == "주식체결"):
                현재가_str = self.ocx.dynamicCall("GetCommRealData(QString, int)", "주식체결", 10)
                현재가 = int(현재가_str.strip())
                if 현재가 < 0:
                    현재가 = 현재가 * (-1)

                balance = self.data.get_balance(sJongmokCode)
                balance.현재가 = 현재가

                for 매수전략 in balance.매수전략.values():
                    매수전략.on_real_data(sJongmokCode, sRealType, sRealData)

                for 매도전략 in balance.매도전략.values():
                    매도전략.on_real_data(sJongmokCode, sRealType, sRealData)

    def OnReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        MyLogger.instance().logger().info("%s, %s, %s, %s", strCode, strType, strConditionName, strConditionIndex)
        condition = self.data.get_condition(int(strConditionIndex))
        balance = self.data.get_balance(strCode)

        if strType == 'I':  # 조건식 편입
            if condition.신호종류 == "매도신호":
                for 매도전략 in balance.매도전략.values():
                    매도전략.on_condition(int(strConditionIndex), strConditionName)

            elif condition.신호종류 == "매수신호":
                pass

        elif strType == 'D':  # 조건식 이탈
            pass

    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        MyLogger.instance().logger().info("%s, %s, %s, %s", sScrNo, sRQName, sTrCode, sMsg)

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        MyLogger.instance().logger().info("%s, %d, %s", sGubun, nItemCnt, sFidList)
        fid_str_list = sFidList.split(";")
        for fid_str in fid_str_list:
            ret = self.ocx.dynamicCall("GetChejanData(int)", int(fid_str))
            MyLogger.instance().logger().info("\t %s: %s", fid_str, ret)

        if sGubun == '0':  # 주문접수 or 주문체결
            MyLogger.instance().logger().info("주문체결통보. sGubun: '0'")
            주문상태 = self.ocx.dynamicCall("GetChejanData(int)", 913)
            매도수구분 = self.ocx.dynamicCall("GetChejanData(int)", 907)  # "1":매도, "2":매수
            종목명 = self.ocx.dynamicCall("GetChejanData(int)", 302)
            주문수량_str = self.ocx.dynamicCall("GetChejanData(int)", 900)
            주문가격_str = self.ocx.dynamicCall("GetChejanData(int)", 901)
            체결가격_str = self.ocx.dynamicCall("GetChejanData(int)", 910)
            체결수량_str = self.ocx.dynamicCall("GetChejanData(int)", 911)
            MyLogger.instance().logger().info("주문상태: %s, 매도수구분: %s, 종목명: %s, 주문수량: %s, 체결가격: %s, 체결수량: %s", 주문상태, 매도수구분, 종목명, 주문수량_str, 주문가격_str, 체결가격_str, 체결수량_str)

        elif sGubun == '1':  # 잔고통보
            MyLogger.instance().logger().info("잔고통보. sGubun: '1'")
            종목코드 = self.ocx.dynamicCall("GetChejanData(int)", 9001)
            현재가_str = self.ocx.dynamicCall("GetChejanData(int)", 10)
            보유수량_str = self.ocx.dynamicCall("GetChejanData(int)", 930)
            매입단가_str = self.ocx.dynamicCall("GetChejanData(int)", 931)
            종목코드 = 종목코드.strip()
            현재가 = int(현재가_str.strip())
            현재가 = 현재가 if 현재가 < 0 else 현재가*(-1)
            매입단가 = int(매입단가_str.strip())
            보유수량 = int(보유수량_str.strip())
            잔고_dic = self.data.잔고_dic

            balance = self.data.get_balance(종목코드)
            balance.현재가 = 현재가
            balance.매입가 = 매입단가
            balance.보유수량 = 보유수량

            if 보유수량 == 0:  # 해당 종목 청산
                del 잔고_dic[종목코드]
                self.set_real_remove(종목코드)  # 실시간 해제

            else:  # 종목 매수
                MyLogger.instance().logger().info("종목 매수")
                for condition in self.data.조건식_dic:
                    if condition.적용유무 == "1":
                        MyLogger.instance().logger().info("조건식 실시간 재등록")
                        self.send_condition(condition)  # 조건식 실시간 재등록

                MyLogger.instance().logger().info("실시간 등록")
                self.set_real_reg(종목코드)  # 실시간 등록

        elif sGubun == '3':  # 특이신호
            MyLogger.instance().logger().warnning("특이신호. sGubun: 3")
            pass

    def OnEventConnect(self, nErrCode):
        if nErrCode == 0:
            MyLogger.instance().logger().info("로그인 성공")
            account_num = self.ocx.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
            account_num = account_num[:-1]
            account_list = account_num.split(";")
            self.data.계좌번호_list = account_list
            self.data.계좌번호 = account_list[0]
            self.callback.on_data_updated(["계좌번호"])
            self.callback.on_connected()

    def OnReceiveCondition(self, strCode, strType, strConditionName, strConditionIndex):
        MyLogger.instance().logger().info("%s, %s, %s, %s", strCode, strType, strConditionName, strConditionIndex)

    def OnReceiveTrCondition(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        MyLogger.instance().logger().info("%s, %s, %s, %d, %d", sScrNo, strCodeList, strConditionName, nIndex, nNext)
        code_list_str = strCodeList[:-1]  # 마지막 ";" 제거
        code_list = code_list_str.split(';')
        MyLogger.instance().logger().info("code_list: %s", code_list)
        for code in code_list:
            name = self.ocx.dynamicCall("GetMasterCodeName(QString)", [code])
            MyLogger.instance().logger().info("code: %s, name: %s", code, name)

    def OnReceiveConditionVer(self, lRet, sMsg):
        MyLogger.instance().logger().info("%d %s", lRet, sMsg)
        condition_ret = self.ocx.dynamicCall("GetConditionNameList()")
        condition_ret = condition_ret[:-1]  # 마지막 ";" 제거
        condition_list_raw = condition_ret.split(";")
        self.data.조건식_dic.clear()
        for condition_with_index in condition_list_raw:
            if condition_with_index == "":
                continue
            cur = condition_with_index.split("^")
            인덱스 = int(cur[0])
            조건명 = cur[1]
            condition_instance = self.data.get_condition(인덱스)
            condition_instance.조건명 = 조건명
        self.callback.on_data_updated(["조건식_dic"])

    ##############################################################
    # Functions
    ##############################################################

    def login(self):
        MyLogger.instance().logger().info("")
        if self.ocx.dynamicCall("GetConnectState()") == 0:
            self.ocx.dynamicCall("CommConnect()")

    def refresh_condition_dic(self):
        MyLogger.instance().logger().info("")
        ret = self.ocx.dynamicCall("GetConditionLoad()")
        MyLogger.instance().logger().info("call GetConditionLoad(). ret: %d", ret)

    def send_condition(self, the_condition):
        MyLogger.instance().logger().info("%s, %s, %s", the_condition.조건명, the_condition.신호종류, the_condition.적용유무)
        screen_num = constant.SN_조건식_미지정
        if the_condition.신호종류 == "매수신호":
            screen_num = constant.SN_조건식_매수신호
        elif the_condition.신호종류 == "매도신호":
            screen_num = constant.SN_조건식_매도신호
        if the_condition.적용유무 == "1":
            MyLogger.instance().logger().info("call send_condition_stop first")
            self.send_condition_stop(screen_num, the_condition.조건명, the_condition.인덱스)

        MyLogger.instance().logger().info("param for SendCondition(). SN: %s, 조건명: %s, 인덱스: %d, 적용유무: %d", screen_num, the_condition.조건명, the_condition.인덱스, int(the_condition.적용유무))
        ret = self.ocx.dynamicCall("SendCondition(QString, QString, int, int)", screen_num, the_condition.조건명, the_condition.인덱스, int(the_condition.적용유무))
        MyLogger.instance().logger().info("call SendCondition(). ret: %d", ret)
        return ret

    def send_condition_stop(self, the_화면번호, the_조건명, the_조건명인덱스):
        MyLogger.instance().logger().info("%s, %s, %d", the_화면번호, the_조건명, the_조건명인덱스)
        self.ocx.dynamicCall("SendConditionStop(QString, QString, int)", the_화면번호, the_조건명, the_조건명인덱스)
        MyLogger.instance().logger().info("call SendConditionStop()")

    def tr_balance(self):
        MyLogger.instance().logger().info("계좌번호 %s", self.data.계좌번호)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.data.계좌번호)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "조회구분", 2)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", 0, constant.SN_잔고조회)

    def tr_code(self, the_종목코드):
        MyLogger.instance().logger().info("the_종목코드 %s", the_종목코드)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", the_종목코드)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", 0, constant.SN_종목정보)

    def set_real_reg(self, the_종목코드_list_str):
        MyLogger.instance().logger().info("the_종목코드_list_str %s", the_종목코드_list_str)
        fid = "9001;10;13"  # 종목코드,업종코드;현재가;누적거래량
        ret = self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                                   [constant.SN_실시간조회, the_종목코드_list_str, fid, "1"])  # "1" 종목 추가, "0" 기존 종목은 제외
        MyLogger.instance().logger().info("call SetRealReg(). ret: %d", ret)
        return ret

    def set_real_remove(self, the_종목코드):
        MyLogger.instance().logger().info("the_종목코드 %s", the_종목코드)
        ret = self.ocx.dynamicCall("SetRealRemove(QString, QString)", [constant.SN_실시간조회, the_종목코드])
        MyLogger.instance().logger().info("call SetRealRemove(). ret: %d", ret)
        return ret

    def send_order(self, 주문유형, 종목코드, 주문수량, 주문단가, 거래구분):
        MyLogger.instance().logger().info("%d, %s, %d, %d, %s", 주문유형, 종목코드, 주문수량, 주문단가, 거래구분)
        sRQName = "주식주문"
        sScreenNo = constant.SN_주식주문
        ret = self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                   [sRQName, sScreenNo, self.data.계좌번호, 주문유형, 종목코드, 주문수량, 주문단가, 거래구분, ""])
        MyLogger.instance().logger().info("call SendOrder(). ret: %d", ret)
        return ret


class KiwoomCallback:
    def on_connected(self):
        pass

    def on_data_updated(self, key_list):
        pass

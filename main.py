import sys
from PyQt4.QAxContainer import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import kiwoom_util
import ui

gMyData = {"조건식_list": [[0, "조건식0", "매도신호", False]],  # [인덱스, 조건명, 신호종류, 적용유무]
           "계좌번호": "12345",
           "잔고_dic": {"00000": {"종목명": "테스트0", "현재가": 2000, "매입가": 1000, "수익율": 0.5, "매수전략": True, "매도전략": True},
                      "00001": {"종목명": "테스트1", "현재가": 2000, "매입가": 1000, "수익율": 0.5, "매수전략": False, "매도전략": False}
                      },
           }

def OnReceiveTrData(sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
    print("(OnReceiveTrData) ", sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg)
    if sRQName == "주식기본정보요청":
        name = gOcx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "종목명")
        volume = gOcx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, 0, "거래량")
        retStr = ""
        retStr += "종목명: " + name.strip() + "\n"
        retStr += "거래량: " + volume.strip() + "\n"
        gWindow.on_print(retStr)

    elif sRQName == "계좌평가잔고내역요청":
        print("계좌평가잔고내역요청")
        count = gOcx.dynamicCall("GetDataCount(QString)", ["계좌평가잔고개별합산"])
        print("count: ", count)
        잔고_dic = gMyData["잔고_dic"]
        잔고_dic.clear()
        for i in range(0, count):
            code = gOcx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "종목번호")
            name = gOcx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "종목명")
            cur_price = gOcx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "현재가")
            buy_price = gOcx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "매입가")
            earnings_rate = gOcx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sTrCode, "", sRQName, i, "수익률(%)")
            code = code.strip()
            name = name.strip()
            cur_price = int(cur_price.strip())
            buy_price = int(buy_price.strip())
            earnings_rate = float(earnings_rate.strip())
            earnings_rate /= 100
            print("수익률", earnings_rate)
            print(name, "현재가: ", cur_price, "매입가: ", buy_price, "수익률: ", earnings_rate)
            잔고_dic[code] = {"종목명": name, "현재가": cur_price, "매입가": buy_price, "수익율": earnings_rate, "매수전략": True, "매도전략": True}
        gWindow.on_my_data_updated(["잔고_dic"])


def OnReceiveRealData(sJongmokCode, sRealType, sRealData):
    print("(OnReceiveRealData) ", sJongmokCode, ", ", sRealType, ", ", sRealData)
    잔고_dic = gMyData["잔고_dic"]
    if sJongmokCode in 잔고_dic:
        매수전략_list = 잔고_dic[sJongmokCode]["매수전략"]
        for 매수전략 in 매수전략_list:
            매수전략.onRealData(sJongmokCode, sRealType, sRealData)

        매도전략_list = 잔고_dic[sJongmokCode]["매도전략"]
        for 매도전략 in 매도전략_list:
            매도전략.onRealData(sJongmokCode, sRealType, sRealData)


def OnReceiveMsg(sScrNo, sRQName, sTrCode, sMsg):
    print("(OnReceiveMsg) ", sScrNo, sRQName, sTrCode, sMsg)


def OnReceiveChejanData(sGubun, nItemCnt, sFidList):
    print("(OnReceiveChejanData) ", sGubun, nItemCnt, sFidList)


def OnEventConnect(nErrCode):
    if nErrCode == 0:
        print("로그인 성공")
        gWindow.on_print("로그인 성공")
        gWindow.statusBar().showMessage("Connected")
        account_num = gOcx.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        account_num = account_num[:-1]
        account_list = account_num.split(";")
        gMyData["계좌번호"] = account_list[0]
        gWindow.on_my_data_updated(["계좌번호"])

def OnReceiveCondition(strCode, strType, strConditionName, strConditionIndex):
    print("(OnReceiveCondition) ", strCode, strType, strConditionName, strConditionIndex)


def OnReceiveTrCondition(sScrNo, strCodeList, strConditionName, nIndex, nNext):
    print("(OnReceiveTrCondition) ", sScrNo, strCodeList, strConditionName, nIndex, nNext)
    strCodeList = strCodeList[:-1]  # 마지막 ";" 제거
    codeList = strCodeList.split(';')
    print(codeList)
    for code in codeList:
        name = gOcx.dynamicCall("GetMasterCodeName(QString)", [code])
        print(name)


def OnReceiveConditionVer(lRet, sMsg):
    print("(OnReceiveConditionVer) ", lRet, sMsg)
    condition_ret = gOcx.dynamicCall("GetConditionNameList()")
    condition_ret = condition_ret[:-1]  # 마지막 ";" 제거
    print(condition_ret)
    condition_list_raw = condition_ret.split(";")
    print(condition_list_raw)
    condition_list = gMyData["조건식_list"]
    condition_list.clear()
    for condition_with_index in condition_list_raw:
        if condition_with_index == "":
            continue
        cur = condition_with_index.split("^")
        cur_list = [int(cur[0]), cur[1], "미지정", False]
        condition_list.append(cur_list)
    print(condition_list)
    gWindow.on_my_data_updated(["조건식_list"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gOcx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    gOcx.connect(gOcx, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), OnReceiveTrData)
    gOcx.connect(gOcx, SIGNAL("OnReceiveRealData(QString, QString, QString)"), OnReceiveRealData)
    gOcx.connect(gOcx, SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"), OnReceiveMsg)
    gOcx.connect(gOcx, SIGNAL("OnReceiveChejanData(QString, int, QString)"), OnReceiveChejanData)
    gOcx.connect(gOcx, SIGNAL("OnEventConnect(int)"), OnEventConnect)
    gOcx.connect(gOcx, SIGNAL("OnReceiveCondition(QString, QString, QString, QString)"), OnReceiveCondition)
    gOcx.connect(gOcx, SIGNAL("OnReceiveTrCondition(QString, QString, QString, int, int)"), OnReceiveTrCondition)
    gOcx.connect(gOcx, SIGNAL("OnReceiveConditionVer(int, QString)"), OnReceiveConditionVer)

    gKiwoomUtil = kiwoom_util.KiwoomUtil(gOcx, gMyData)
    gKiwoomUtil.login()

    gWindow = ui.MyWindow(gKiwoomUtil, gMyData)
    gWindow.show()
    app.exec_()
    print("after exec ")



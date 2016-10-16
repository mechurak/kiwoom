import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from kiwoom.kiwoom import Kiwoom
from kiwoom.kiwoom import KiwoomCallback
from kiwoom.data import Condition
from kiwoom.data import Balance
from logger import MyLogger
import json


class ConditionItem:
    def __init__(self, the_condition):
        self.condition = the_condition
        self.button = QPushButton("조회 및 요청")
        self.button.clicked.connect(lambda: kiwoom.send_condition(self.condition))


class MyWindow(QMainWindow, KiwoomCallback):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('window.ui', self)
        self.ui.table_current.setHorizontalHeaderLabels(["test1", "test2", "test3"])
        self.ui.table_current.setItem(0, 0, QTableWidgetItem("test"))
        self.ui.table_current.setItem(0, 1, QTableWidgetItem("test0_1"))
        self.ui.table_current.setItem(1, 0, QTableWidgetItem("test1_0"))
        self.ui.table_current.itemChanged.connect(self.on_balance_item_changed)
        vertical_header = self.ui.table_current.verticalHeader()
        vertical_header.connect(vertical_header, SIGNAL("sectionClicked(int)"), self.on_balance_section_clicked)
        self.is_user_changing_balance = False
        self.selected_balance = []
        self.ui.combo_buy.addItems(Balance.get_available_buy_strategy())
        self.ui.combo_sell.addItems(Balance.get_available_sell_strategy())
        condition_vertical_header = self.ui.table_condition.verticalHeader()
        condition_vertical_header.connect(condition_vertical_header, SIGNAL("sectionClicked(int)"), self.on_condition_section_clicked)
        self.selected_condition = []
        self.ui.combo_signal.addItems(Condition.get_signal_type_items_list())
        self.ui.combo_apply.addItems(Condition.get_applied_items_list())

    @pyqtSlot(str)
    def on_account_changed(self, account):
        MyLogger.instance().logger().info("account: %s", account)
        kiwoom.data.계좌번호 = account

    @pyqtSlot()
    def on_condition_refresh_btn_clicked(self):
        MyLogger.instance().logger().info("")
        kiwoom.refresh_condition_dic()

    @pyqtSlot()
    def on_condition_result_add_btn_clicked(self):
        MyLogger.instance().logger().info("")
        code_text = self.ui.txt_condition_result.toPlainText()
        if len(code_text) > 4:
            code_list = (eval(code_text))
            code_list_str = ";".join(code_list)
            kiwoom.tr_multi_code(code_list_str, len(code_list))
        else:
            MyLogger.instance().logger().error("self.ui.txt_condition_result is too short.")

    @pyqtSlot()
    def on_balance_btn_clicked(self):
        MyLogger.instance().logger().info("")
        kiwoom.tr_balance()

    @pyqtSlot()
    def on_interest_balance_btn_clicked(self):
        MyLogger.instance().logger().info("")
        kiwoom.refresh_interest_balance()

    @pyqtSlot()
    def on_print_my_data_btn_clicked(self):
        MyLogger.instance().logger().info("")
        kiwoom.data.print()

    @pyqtSlot()
    def on_code_btn_clicked(self):
        MyLogger.instance().logger().info("code: %s", self.ui.edit_code.text())
        kiwoom.tr_code(self.ui.edit_code.text())

    @pyqtSlot()
    def on_code_del_btn_clicked(self):
        MyLogger.instance().logger().info("")
        for balance in self.selected_balance:
            del kiwoom.data.잔고_dic[balance.종목코드]
        self.on_data_updated(["잔고_dic"])

    @pyqtSlot()
    def on_register_real_all_btn_clicked(self):
        MyLogger.instance().logger().info("")
        잔고_dic = kiwoom.data.잔고_dic
        종목코드_list = 잔고_dic.keys()
        종목코드_list_str = ";".join(종목코드_list)
        MyLogger.instance().logger().info("종목코드_list_str %s", 종목코드_list_str)
        kiwoom.set_real_reg(종목코드_list_str)

    @pyqtSlot()
    def on_buy_strategy_add_btn_clicked(self):
        strategy_str = self.ui.combo_buy.currentText()
        MyLogger.instance().logger().info("전략: %s", strategy_str)
        for balance in self.selected_balance:
            param = eval(self.ui.txt_buy_param.text())
            if not type(param) == dict:
                MyLogger.instance().logger().error("wrong param text: %s", self.ui.txt_buy_param.text())
                param = {}
            balance.add_buy_strategy(strategy_str, param)
        self.on_data_updated(["잔고_dic"])

    @pyqtSlot()
    def on_sell_strategy_add_btn_clicked(self):
        strategy_str = self.ui.combo_sell.currentText()
        MyLogger.instance().logger().info("전략: %s", strategy_str)
        for balance in self.selected_balance:
            param = eval(self.ui.txt_sell_param.text())
            if not type(param) == dict:
                MyLogger.instance().logger().error("wrong param text: %s", self.ui.txt_sell_param.text())
                param = {}
            balance.add_sell_strategy(strategy_str, param)
        self.on_data_updated(["잔고_dic"])

    @pyqtSlot(str)
    def on_buy_strategy_changed(self, strategy):
        from kiwoom.strategy.just_buy import JustBuy
        from kiwoom.strategy.buy_on_opening import BuyOnOpening
        if strategy == "buy_just_buy":
            default_param = JustBuy.get_default_param()
        elif strategy == "buy_on_opening":
            default_param = BuyOnOpening.get_default_param()
        else:
            MyLogger.instance().logger().warning("unknown strategy. ignore %s", strategy)
        MyLogger.instance().logger().warning("strategy %s, default_param %s", strategy, str(default_param))
        self.ui.txt_buy_param.setText(str(default_param))

    @pyqtSlot(str)
    def on_sell_strategy_changed(self, strategy):
        from kiwoom.strategy.stop_loss import StopLoss
        from kiwoom.strategy.condition_sell import ConditionSell
        from kiwoom.strategy.sell_on_closing import SellOnClosing
        if strategy == "sell_stop_loss":
            default_param = StopLoss.get_default_param()
        elif strategy == "sell_condition_sell":
            default_param = ConditionSell.get_default_param()
        elif strategy == "sell_on_closing":
            default_param = SellOnClosing.get_default_param()
        else:
            MyLogger.instance().logger().warning("unknown strategy. ignore %s", strategy)
        MyLogger.instance().logger().warning("strategy %s, default_param %s", strategy, str(default_param))
        self.ui.txt_sell_param.setText(str(default_param))

    @pyqtSlot()
    def on_buy_strategy_clear_btn_clicked(self):
        MyLogger.instance().logger().info("")
        for balance in self.selected_balance:
            balance.매수전략.clear()
        self.on_data_updated(["잔고_dic"])

    @pyqtSlot()
    def on_sell_strategy_clear_btn_clicked(self):
        MyLogger.instance().logger().info("")
        for balance in self.selected_balance:
            balance.매도전략.clear()
        self.on_data_updated(["잔고_dic"])

    @pyqtSlot()
    def on_load_balance_btn_clicked(self):
        MyLogger.instance().logger().info("")
        f = open("my_list.txt", "r", encoding='utf8')
        data = json.load(f)
        print(data)

        for item in data:
            balance = kiwoom.data.get_balance(item['종목코드'])
            balance.종목명 = item['종목명']
            if not item['목표보유수량']:
                balance.목표보유수량 = item['목표보유수량']
            for k, v in item['매수전략_dic'].items():
                balance.add_buy_strategy(k, v)
            for k, v in item['매도전략_dic'].items():
                balance.add_sell_strategy(k, v)

        self.on_data_updated(["잔고_dic"])
        kiwoom.refresh_interest_balance()

    @pyqtSlot()
    def on_save_balance_btn_clicked(self):
        MyLogger.instance().logger().info("")
        f = open("my_list.txt", "w", encoding='utf8')
        list_data = []
        for balance in kiwoom.data.잔고_dic.values():
            list_data.append(balance.get_dic())
        data = json.dumps(list_data, ensure_ascii=False, indent=4)
        f.write(data)
        f.close()

    @pyqtSlot()
    def on_test_btn_clicked(self):
        MyLogger.instance().logger().info("")
        kiwoom.perform_test()

    def on_connected(self):
        self.statusBar().showMessage("Connected")

    def on_data_updated(self, key_list):
        if "계좌번호" in key_list:
            계좌번호 = kiwoom.data.계좌번호
            계좌번호_list = kiwoom.data.계좌번호_list
            self.ui.combo_account.clear()
            self.ui.combo_account.addItems(계좌번호_list)
            self.ui.combo_account.setCurrentIndex(self.ui.combo_account.findText(계좌번호))

        if "조건식_dic" in key_list:
            headers = Condition.get_table_header()
            self.ui.table_condition.setColumnCount(len(headers))
            self.ui.table_condition.setHorizontalHeaderLabels(headers)
            self.ui.table_condition.setRowCount(len(kiwoom.data.조건식_dic))

            i = 0
            for condition in kiwoom.data.조건식_dic.values():
                condition_item = ConditionItem(condition)
                self.ui.table_condition.setItem(i, 0, QTableWidgetItem(str(condition.인덱스)))
                self.ui.table_condition.setItem(i, 1, QTableWidgetItem(condition.조건명))
                self.ui.table_condition.setItem(i, 2, QTableWidgetItem(condition.신호종류))
                self.ui.table_condition.setItem(i, 3, QTableWidgetItem(condition.적용유무))
                self.ui.table_condition.setCellWidget(i, 4, condition_item.button)
                i += 1
            kiwoom.data.print()

        if "잔고_dic" in key_list:
            self.is_user_changing_balance = False
            headers = Balance.get_table_header()
            self.ui.table_current.clear()
            self.ui.table_current.setColumnCount(len(headers))
            self.ui.table_current.setHorizontalHeaderLabels(headers)
            self.ui.table_current.setRowCount(len(kiwoom.data.잔고_dic))
            #self.selected_balance.clear()
            #self.ui.txt_balance.clear()

            i = 0
            for balance in kiwoom.data.잔고_dic.values():
                str_list = balance.get_str_list()
                for j in range(0, len(str_list)):
                    self.ui.table_current.setItem(i, j, QTableWidgetItem(str(str_list[j])))
                i += 1

            self.is_user_changing_balance = True
            kiwoom.data.print()

    def on_condition_search_result(self, code_list):
        self.ui.txt_condition_result.setText(str(code_list))

    def on_balance_item_changed(self, item):
        if not self.is_user_changing_balance:
            return
        row = item.row()
        col = item.column()
        value = item.text()
        MyLogger.instance().logger().info("row:%d, col:%d, val:%s", row, col, value)

        종목코드_item = self.ui.table_current.item(row, 0)
        종목코드 = 종목코드_item.text()
        balance = kiwoom.data.get_balance(종목코드)
        changed_key = Balance.get_table_header()[col]
        if changed_key == "목표보유수량":
            balance.목표보유수량 = int(value)
        else:
            return

    def on_balance_section_clicked(self, row):
        MyLogger.instance().logger().info("row: %d", row)
        rows = []
        for idx in self.ui.table_current.selectedIndexes():
            current_row = idx.row()
            if current_row not in rows:
                rows.append(current_row)

        self.selected_balance.clear()
        for row in rows:
            종목코드_item = self.ui.table_current.item(row, 0)
            if not 종목코드_item:  # 빈칸(None)인 경우
                continue
            종목코드 = 종목코드_item.text()
            balance = kiwoom.data.get_balance(종목코드)
            self.selected_balance.append(balance)

        종목명_list = []
        for balance in self.selected_balance:
            종목명_list.append(balance.종목명)
        selected_balance_str = ",".join(종목명_list)
        self.ui.txt_balance.setText(selected_balance_str)

    def on_condition_section_clicked(self, row):
        MyLogger.instance().logger().info("row: %d", row)
        rows = []
        for idx in self.ui.table_condition.selectedIndexes():
            current_row = idx.row()
            if current_row not in rows:
                rows.append(current_row)

        self.selected_condition.clear()
        for row in rows:

            인덱스_item = self.ui.table_condition.item(row, 0)
            if not 인덱스_item:  # 빈칸(None)인 경우
                continue
            인덱스 = int(인덱스_item.text())
            condition = kiwoom.data.get_condition(인덱스)
            self.selected_condition.append(condition)

        조건식_list = []
        for condition in self.selected_condition:
            조건식_list.append(condition.조건명)
        selected_condition_str = ",".join(조건식_list)
        self.ui.txt_condition_select.setText(selected_condition_str)


    @pyqtSlot()
    def on_condition_signal_btn_clicked(self):
        MyLogger.instance().logger().info("")
        signal_str = self.ui.combo_signal.currentText()
        MyLogger.instance().logger().info("신호종류: %s", signal_str)
        for condition in self.selected_condition:
            condition.신호종류 = signal_str
        self.on_data_updated(["조건식_dic"])

    @pyqtSlot()
    def on_condition_apply_btn_clicked(self):
        MyLogger.instance().logger().info("")
        apply_str = self.ui.combo_apply.currentText()
        MyLogger.instance().logger().info("신호종류: %s", apply_str)
        for condition in self.selected_condition:
            condition.적용유무 = apply_str
        self.on_data_updated(["조건식_dic"])

        #def tick(self):
    #    print("tick")

if __name__ == "__main__":
    MyLogger.instance().logger().info("\n\n============================ start application =====================")
    app = QApplication(sys.argv)
    window = MyWindow()
    kiwoom = Kiwoom.instance()
    kiwoom.set_callback(window)
    window.show()
    #timer = QTimer()
    #timer.timeout.connect(window.tick)
    #timer.start(5000)
    app.exec_()

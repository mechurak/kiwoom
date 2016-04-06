import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

class MyWindow(QMainWindow):
    def __init__(self, kiwoom_util, my_data):
        super().__init__()
        self.ui = uic.loadUi('test.ui', self)
        self.kiwoom_util = kiwoom_util
        self.my_data = my_data
        self.ui.table_current.setHorizontalHeaderLabels(["test1", "test2", "test3"])
        self.ui.table_current.setItem(0, 0, QTableWidgetItem("test"))
        self.ui.table_current.setItem(0, 1, QTableWidgetItem("test0_1"))
        self.ui.table_current.setItem(1, 0, QTableWidgetItem("test1_0"))

    @pyqtSlot(str)
    def on_account_changed(self, account):
        print("on_account_changed" + account)
        self.my_data["계좌번호"] = account

    @pyqtSlot()
    def on_condition_refresh_btn_clicked(self):
        print("on_condition_refresh_clicked")
        self.kiwoom_util.refresh_condition_dic()

    @pyqtSlot()
    def on_balance_btn_clicked(self):
        print("on_balance_btn_clicked")
        self.kiwoom_util.tr_balance()

    @pyqtSlot()
    def on_print_my_data_btn_clicked(self):
        print("\n========== my data ==============")
        for key, data in self.my_data.items():
            print(" (" + key + ") ", data)

    @pyqtSlot()
    def on_code_btn_clicked(self):
        print("on_code_btn_clicked")
        print("text(): " + self.ui.edit_code.text())
        self.kiwoom_util.tr_code(self.ui.edit_code.text())

    @pyqtSlot()
    def on_register_real_btn_clicked(self):
        print("on_register_real_btn_clicked")
        print("text(): " + self.ui.edit_code.text())
        self.kiwoom_util.set_real_reg(self.ui.edit_code.text())

    @pyqtSlot()
    def on_register_real_all_btn_clicked(self):
        print("on_register_real_all_btn_clicked")
        잔고_dic = self.my_data["잔고_dic"]
        잔고코드_list = 잔고_dic.keys()
        잔고코드_list_str = ";".join(잔고코드_list)
        print("잔고코드_list_str", 잔고코드_list_str)
        self.kiwoom_util.set_real_reg(잔고코드_list_str)

    def on_connected(self):
        account_list = self.my_data["계좌번호"]
        self.ui.combo_account.addItems(account_list)

    def on_my_data_updated(self, key_list):
        if "계좌번호" in key_list:
            account = self.my_data["계좌번호"]
            self.ui.edit_account.setText(account)

        if "조건식_list" in key_list:
            condition_list = self.my_data["조건식_list"]
            for i in range(0, len(condition_list)):
                self.ui.table_condition.setItem(i, 0, QTableWidgetItem(str(condition_list[i][0])))
                self.ui.table_condition.setItem(i, 1, QTableWidgetItem(condition_list[i][1]))

                combo_box_signal = QComboBox()
                combo_box_signal.addItems(["매도신호", "매수신호", "미지정"])
                combo_box_signal.setCurrentIndex(combo_box_signal.findText(condition_list[i][2]))
                self.ui.table_condition.setCellWidget(i, 2, combo_box_signal)

                combo_box_apply = QComboBox()
                combo_box_apply.addItems(["True", "False"])
                combo_box_apply.setCurrentIndex(combo_box_apply.findText(str(condition_list[i][3])))
                self.ui.table_condition.setCellWidget(i, 3, combo_box_apply)

                button = QPushButton("요청")
                self.ui.table_condition.setCellWidget(i, 4, button)

        if "잔고_dic" in key_list:
            balance_dic = self.my_data["잔고_dic"]
            headers = list(list(balance_dic.values())[0].keys())
            self.ui.table_current.setColumnCount(len(headers))
            self.ui.table_current.setHorizontalHeaderLabels(headers)
            balance_list = list(balance_dic.values())
            for i in range(0, len(balance_list)):
                cur_list = list(balance_list[i].values())
                for j in range(0, len(cur_list)):
                    self.ui.table_current.setItem(i, j, QTableWidgetItem(str(cur_list[j])))

    def on_print(self, log_str):
        self.ui.txt_output.append(log_str)


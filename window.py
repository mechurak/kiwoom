import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from kiwoom.kiwoom import Kiwoom
from kiwoom.kiwoom import KiwoomCallback


class MyWindow(QMainWindow, KiwoomCallback):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('window.ui', self)
        self.ui.table_current.setHorizontalHeaderLabels(["test1", "test2", "test3"])
        self.ui.table_current.setItem(0, 0, QTableWidgetItem("test"))
        self.ui.table_current.setItem(0, 1, QTableWidgetItem("test0_1"))
        self.ui.table_current.setItem(1, 0, QTableWidgetItem("test1_0"))

    @pyqtSlot(str)
    def on_account_changed(self, account):
        print("on_account_changed" + account)
        kiwoom.data["계좌번호"] = account

    @pyqtSlot()
    def on_condition_refresh_btn_clicked(self):
        print("on_condition_refresh_clicked")
        kiwoom.refresh_condition_dic()

    @pyqtSlot()
    def on_balance_btn_clicked(self):
        print("on_balance_btn_clicked")
        kiwoom.tr_balance()

    @pyqtSlot()
    def on_print_my_data_btn_clicked(self):
        print("\n========== my data ==============")
        for key, data in kiwoom.data.items():
            print(" (" + key + ") ", data)

    @pyqtSlot()
    def on_code_btn_clicked(self):
        print("on_code_btn_clicked")
        print("text(): " + self.ui.edit_code.text())
        kiwoom.tr_code(self.ui.edit_code.text())

    @pyqtSlot()
    def on_register_real_btn_clicked(self):
        print("on_register_real_btn_clicked")
        print("text(): " + self.ui.edit_code.text())
        kiwoom.set_real_reg(self.ui.edit_code.text())

    @pyqtSlot()
    def on_register_real_all_btn_clicked(self):
        print("on_register_real_all_btn_clicked")
        잔고_dic = kiwoom.data["잔고_dic"]
        잔고코드_list = 잔고_dic.keys()
        잔고코드_list_str = ";".join(잔고코드_list)
        print("잔고코드_list_str", 잔고코드_list_str)
        kiwoom.set_real_reg(잔고코드_list_str)

    def on_connected(self):
        self.statusBar().showMessage("Connected")

    def on_data_updated(self, key_list):
        if "계좌번호" in key_list:
            계좌번호 = kiwoom.data["계좌번호"]
            계좌번호_list = kiwoom.data["계좌번호_list"]
            self.ui.combo_account.clear()
            self.ui.combo_account.addItems(계좌번호_list)
            self.ui.combo_account.setCurrentIndex(self.ui.combo_account.findText(계좌번호))

        if "조건식_list" in key_list:
            condition_list = kiwoom.data["조건식_list"]
            headers = kiwoom.data["조건식_list_header"]
            self.ui.table_condition.setColumnCount(len(headers))
            self.ui.table_condition.setHorizontalHeaderLabels(headers)

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
            balance_dic = kiwoom.data["잔고_dic"]
            headers = kiwoom.data["잔고_dic_header"]
            self.ui.table_current.clear()
            self.ui.table_current.setColumnCount(len(headers))
            self.ui.table_current.setHorizontalHeaderLabels(headers)
            balance_list = list(balance_dic.values())

            for i in range(0, len(balance_list)):
                self.ui.table_current.setItem(i, 0, QTableWidgetItem(balance_list[i][0]))  # 종목명
                self.ui.table_current.setItem(i, 1, QTableWidgetItem(str(balance_list[i][1])))  # 현재가
                self.ui.table_current.setItem(i, 2, QTableWidgetItem(str(balance_list[i][2])))  # 매입가
                self.ui.table_current.setItem(i, 3, QTableWidgetItem(str(balance_list[i][3])))  # 보유수량
                self.ui.table_current.setItem(i, 4, QTableWidgetItem(str(balance_list[i][4])))  # 수익율
                self.ui.table_current.setItem(i, 5, QTableWidgetItem(str(balance_list[i][5])))  # 매수전략
                self.ui.table_current.setItem(i, 6, QTableWidgetItem(str(balance_list[i][6])))  # 매도전략

    def on_print(self, log_str):
        self.ui.txt_output.append(log_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    kiwoom = Kiwoom(window)
    window.show()
    app.exec_()

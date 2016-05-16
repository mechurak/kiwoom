import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from kiwoom.kiwoom import Kiwoom
from kiwoom.kiwoom import KiwoomCallback


class Condition:
    def __init__(self, i, 조건식):
        self.i = i
        self.조건식 = 조건식

        self.combo_box_signal = QComboBox()
        self.combo_box_signal.addItems(["매도신호", "매수신호", "미지정"])
        self.combo_box_signal.setCurrentIndex(self.combo_box_signal.findText(self.조건식[2]))
        self.combo_box_signal.connect(self.combo_box_signal, SIGNAL("currentIndexChanged(QString)"), self.on_signal_changed)

        self.combo_box_apply = QComboBox()
        self.combo_box_apply.addItems(["True", "False"])
        self.combo_box_apply.setCurrentIndex(self.combo_box_apply.findText(str(self.조건식[3])))
        self.combo_box_apply.connect(self.combo_box_apply, SIGNAL("currentIndexChanged(QString)"), self.on_apply_changed)

        self.button = QPushButton("요청")
        적용유무 = 0
        if self.조건식[3]:
            적용유무 = 1
        self.button.clicked.connect(lambda: kiwoom.tr_condition_result(self.조건식[1], self.조건식[0], self.조건식[2], 적용유무))

    def on_signal_changed(self, 신호종류):
        self.조건식[2] = 신호종류

    def on_apply_changed(self, 적용유무):
        self.조건식[3] = 적용유무


class MyWindow(QMainWindow, KiwoomCallback):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('window.ui', self)
        self.ui.table_current.setHorizontalHeaderLabels(["test1", "test2", "test3"])
        self.ui.table_current.setItem(0, 0, QTableWidgetItem("test"))
        self.ui.table_current.setItem(0, 1, QTableWidgetItem("test0_1"))
        self.ui.table_current.setItem(1, 0, QTableWidgetItem("test1_0"))
        self.ui.table_current.itemChanged.connect(self.on_balance_item_changed)
        self.is_listening = False

    @pyqtSlot(str)
    def on_account_changed(self, account):
        print("on_account_changed" + account)
        kiwoom.data.계좌번호 = account

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
        kiwoom.data.print()

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
        잔고_dic = kiwoom.data.잔고_dic
        잔고코드_list = 잔고_dic.keys()
        잔고코드_list_str = ";".join(잔고코드_list)
        print("잔고코드_list_str", 잔고코드_list_str)
        kiwoom.set_real_reg(잔고코드_list_str)

    def on_connected(self):
        self.statusBar().showMessage("Connected")

    def on_data_updated(self, key_list):
        if "계좌번호" in key_list:
            계좌번호 = kiwoom.data.계좌번호
            계좌번호_list = kiwoom.data.계좌번호_list
            self.ui.combo_account.clear()
            self.ui.combo_account.addItems(계좌번호_list)
            self.ui.combo_account.setCurrentIndex(self.ui.combo_account.findText(계좌번호))

        if "조건식_list" in key_list:
            condition_list = kiwoom.data.조건식_list
            headers = kiwoom.data.get_condition_header()
            self.ui.table_condition.setColumnCount(len(headers))
            self.ui.table_condition.setHorizontalHeaderLabels(headers)

            for i in range(0, len(condition_list)):
                condition = Condition(i, condition_list[i])
                self.ui.table_condition.setItem(i, 0, QTableWidgetItem(str(condition_list[i][0])))
                self.ui.table_condition.setItem(i, 1, QTableWidgetItem(condition_list[i][1]))
                self.ui.table_condition.setCellWidget(i, 2, condition.combo_box_signal)
                self.ui.table_condition.setCellWidget(i, 3, condition.combo_box_apply)
                self.ui.table_condition.setCellWidget(i, 4, condition.button)

        if "잔고_dic" in key_list:
            self.is_listening = False
            headers = kiwoom.data.get_balance_header()
            self.ui.table_current.clear()
            self.ui.table_current.setColumnCount(len(headers))
            self.ui.table_current.setHorizontalHeaderLabels(headers)
            balance_list = kiwoom.data.get_balance_list()
            print(balance_list)

            for i in range(0, len(balance_list)):
                cur_list = balance_list[i]
                for j in range(0, len(cur_list)):
                    self.ui.table_current.setItem(i, j, QTableWidgetItem(str(cur_list[j])))

            self.is_listening = True

    def on_balance_item_changed(self, item):
        if not self.is_listening:
            return
        print("on_balance_item_changed")
        row = item.row()
        col = item.column()
        value = item.text()
        print(row, col, value)

        종목번호_item = self.ui.table_current.item(row, 0)
        종목번호 = 종목번호_item.text()
        changed = kiwoom.data.get_balance_header()[col]
        print(종목번호, changed, value)

        cur_balance_dic = {changed: value}
        kiwoom.data.set_balance(종목번호, cur_balance_dic)

    def on_print(self, log_str):
        self.ui.txt_output.append(log_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    kiwoom = Kiwoom(window)
    window.show()
    app.exec_()

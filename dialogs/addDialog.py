from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
import cv2 as cv

from pages.addPage import Add_Ui_Dialog


class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Add_Ui_Dialog()
        self.ui.setupUi(self)
        self.show()

    def set_table_text(self, cp, yz, dh, zz):
        """
        添加表格的一行
        """
        table_widget = self.ui.tableWidget
        row = table_widget.rowCount()
        table_widget.insertRow(row)
        cp_item = QTableWidgetItem(cp)
        yz_item = QTableWidgetItem(yz)
        zz_item = QTableWidgetItem(zz)
        dh_item = QTableWidgetItem(dh)
        table_widget.setItem(row, 0, cp_item)
        table_widget.setItem(row, 1, yz_item)
        table_widget.setItem(row, 2, zz_item)
        table_widget.setItem(row, 3, dh_item)
        table_widget.setRowHeight(row, 100)  # 设置每一行的高度为100像素

    def submit(self):
        """
        提交数据，添加内容
        """
        print(12345)
        cp = self.ui.lineEdit.text()  # 使用 text() 方法从 QLineEdit 中获取文本
        print(cp)
        print(11)
        yz = self.ui.lineEdit_2.text()  # 同样，对于 QLineEdit 使用 text()
        print(yz)
        print(22)
        # 注意：这里您可能也犯了一个错误，使用了两次 self.ui.lineEdit_2
        # 如果 lineEdit_3 是另一个控件，请确保它已正确命名和连接
        dh = self.ui.lineEdit_3.text()  # 假设 lineEdit_3 是另一个 QLineEdit
        print(dh)
        print(33)
        zz = self.ui.lineEdit_4.text()  # 假设 lineEdit_4 是另一个 QLineEdit
        print(zz)
        print(44)
        self.set_table_text(cp, yz, dh, zz)

    def find(self):
        """
        查询
        """
        input = self.ui.lineEdit_5.toPlainText()

    def delete(self):
        """
        删除
        """
        pass

    def navigate_back(self):
        """
        页面跳转
        """
        self.close()
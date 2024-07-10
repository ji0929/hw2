from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog

from dialogs.addDialog import AddDialog
from dialogs.showDialog import ShowDialog
from pages.mainPage import Main_Ui_Dialog


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Main_Ui_Dialog()
        self.ui.setupUi(self)
        self.show()



    def go_show(self):
        """
        页面跳转
        """
        self.show_dialog = ShowDialog()


    def go_add(self):
        """
        页面跳转
        """
        self.add_dialog = AddDialog()

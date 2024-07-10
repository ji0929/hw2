from PyQt5.QtWidgets import QApplication
import sys
from dialogs.mainDialog import MainDialog
class MyApp(QApplication):
    """
    创建应用
    """
    def __init__(self):
        super(MyApp, self).__init__(sys.argv)
        self.md = MainDialog()

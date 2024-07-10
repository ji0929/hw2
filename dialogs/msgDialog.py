from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from data import share_data
from api.video import Video
from pages.msgPage import Msg_Ui_Dialog


class MsgDialog(QDialog):
    def __init__(self, t='today'):
        super().__init__()
        self.type = t
        self.video_path = 'data/video1.mp4'
        self.ui = Msg_Ui_Dialog()
        if self.type == 'today':
            self.ui.setupUi(self, "今日流量")
        else:
            self.ui.setupUi(self, "本周流量")
        self.show_data()
        self.show()

    def set_table_text(self):
        """
        添加表格的一行
        """
        table_widget = self.ui.tableWidget
        for i in range(2):
            # 添加行
            row = table_widget.rowCount()
            table_widget.insertRow(row)
            for j in range(5):
                item = QTableWidgetItem(share_data.data_record[i][j])
                table_widget.setItem(i, j, item)  # 时间列

        for i in range(2):  # 假设您有5行数据
            table_widget.setRowHeight(i, 100)  # 设置每一行的高度为100像素


    def show_img(self, h, w, c, b, i, v_num, nv_num, p_num):
        """
        放置图片/视频
        """
        image = QImage(b, w, h, w * c, QImage.Format_BGR888)
        pix = QPixmap.fromImage(image)
        width = self.ui.label_2.width()
        height = self.ui.label_2.height()
        scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
        self.ui.label_2.setPixmap(scale_pix)


    def show_data(self):
        """
        展示数据
        """
        self.video = Video(self.video_path)
        self.video.send.connect(self.show_img)
        self.video.start()
        self.set_table_text()

    def navigate_back(self):
        self.close()
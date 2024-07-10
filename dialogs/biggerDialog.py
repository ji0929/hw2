from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from api.video import Video
from pages.biggerPage import Bigger_Ui_Dialog
import data.share_data as share_data


class BiggerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.video_path = 'data/video1.mp4'
        self.ui = Bigger_Ui_Dialog()
        self.ui.setupUi(self)
        self.show_data()
        self.show()

    def set_table_text(self,v_num, nv_num, p_num):
        """
        添加表格的一行
        """
        table_widget = self.ui.tableWidget
        type_name = ["people", "motor_vehicle", "non_motor_vehicle"]
        # 添加一些示例数据
        for i in range(3):
            # 添加行
            row = table_widget.rowCount()
            table_widget.insertRow(row)

            name_item = QTableWidgetItem(type_name[i])
            if i == 0:
                num_item = QTableWidgetItem(str(p_num))
                all_item = QTableWidgetItem(str(share_data.num_people_all))
            elif i == 1:
                num_item = QTableWidgetItem(str(v_num))
                all_item = QTableWidgetItem(str(share_data.num_motor_vehicle_all))
            else:
                num_item = QTableWidgetItem(str(nv_num))
                all_item = QTableWidgetItem(str(share_data.num_non_motor_vehicle_all))

            # 将 QTableWidgetItem 对象添加到表格中
            table_widget.setItem(i, 0, name_item)  # 时间列
            table_widget.setItem(i, 1, num_item)  # 信息列
            table_widget.setItem(i, 2, all_item)  # 信息列

        for i in range(3):  # 假设您有5行数据
            table_widget.setRowHeight(i, 100)  # 设置每一行的高度为100像素

    def show_img(self, h, w, c, b, i, v_num, nv_num, p_num):
        """
        放置图片/视频
        """
        image = QImage(b, w, h, w * c, QImage.Format_BGR888)
        pix = QPixmap.fromImage(image)
        width = self.ui.label.width()
        height = self.ui.label.height()
        scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
        self.ui.label.setPixmap(scale_pix)
        self.set_table_text(v_num, nv_num, p_num)

    def show_data(self):
        """
        数据初始化
        """
        self.video = Video(self.video_path)
        self.video.send.connect(self.show_img)
        self.video.start()


    def navigate_back(self):
        """
        页面跳转
        """
        self.close()

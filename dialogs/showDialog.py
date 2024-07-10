from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog
import cv2 as cv

from data import share_data
from api.video import Video
from dialogs.biggerDialog import BiggerDialog
from dialogs.msgDialog import MsgDialog
from dialogs.recordDialog import RecordDialog
from pages.showPage import Show_Ui_Dialog
import matplotlib.pyplot as plt

class ShowDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.video_path = 'data/video1.mp4'
        self.ui = Show_Ui_Dialog()
        self.ui.setupUi(self)
        self.show_data()
        self.show()

    def draw_rect(info, img):
        """
        绘制框，框起机动车和非机动车
        """
        for vehicle in info:
            vehicle_type = vehicle["type"]
            location = vehicle['location']
            x1 = location['left']
            y1 = location['top']
            x2 = x1 + location['width']
            y2 = y1 + location['height']
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            # 定义要绘制的文字
            text = vehicle['type']
            position = (x1, y1 - 2)
            font = cv.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            if vehicle_type in ["car", "bus", "truck"]:
                color = (0, 0, 255)  # 红色
            else:
                color = (255, 0, 0)  # 蓝色
            thickness = 2
            img = cv.putText(img, text, position, font, font_scale, color, thickness, cv.LINE_AA)

        return img

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

    def show_plt(self, path):
        """
        绘制表格
        """
        plt.figure(figsize=(10, 4))  # 宽度为10英寸，高度为5英寸
        if path == 'data/today.png':
            x = range(len(share_data.today_data["v"]))
            width = 0.35  # 条形图的宽度
            plt.bar(x, share_data.today_data["v"], width, label="vehicle")
            plt.bar([p + width for p in x], share_data.today_data["people"], width, label="people")
        else:
            x = range(len(share_data.week_data["v"]))
            width = 0.35  # 条形图的宽度
            plt.bar(x, share_data.week_data["v"], width, label="vehicle")
            plt.bar([p + width for p in x], share_data.week_data["people"], width, label="people")

            # 添加图例
        plt.legend()

        # 添加标题和轴标签
        plt.xlabel("Day")
        plt.ylabel("Value")
        plt.xticks(x, [f"Day {i + 1}" for i in x])  # 如果需要的话，可以添加具体的日期标签

        # 保存图形
        plt.savefig(path)
        plt.close()  # 关闭绘图窗口（如果有的话）

        image = cv.imread(path)
        h, w, c = image.shape
        b = image.tobytes()
        image = QImage(b, w, h, w * c, QImage.Format_BGR888)
        pix = QPixmap.fromImage(image)
        if path == 'data/today.png':
            width = self.ui.label_2.width()
            height = self.ui.label_2.height()
            scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
            self.ui.label_2.setPixmap(scale_pix)
        else:
            width = self.ui.label_2_1.width()
            height = self.ui.label_2_1.height()
            scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
            self.ui.label_2_1.setPixmap(scale_pix)

    def show_data(self):
        """
        展示数据
        """
        self.video = Video(self.video_path)
        self.video.send.connect(self.show_img)
        self.video.start()
        self.show_plt("data/today.png")
        self.show_plt("data/week.png")
        print('enter show page')

    def navigate_back(self):
        """
        页面跳转
        """
        self.close()

    def go_record(self):
        """
        页面跳转
        """
        self.record_dialog = RecordDialog()

    def go_bigger(self):
        """
        页面跳转
        """
        self.bigger_dialog = BiggerDialog()

    def go_msg_1(self):
        """
        页面跳转
        """
        self.msg_dialog_1 = MsgDialog('today')

    def go_msg_2(self):
        """
        页面跳转
        """
        self.msg_dialog_2 = MsgDialog('week')
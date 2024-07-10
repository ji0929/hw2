from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog
import cv2 as cv

from api.video import Video
from pages.recordPage import Record_Ui_Dialog


class RecordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Record_Ui_Dialog()
        self.video_path = ['data/video1.mp4', 'data/video2.mp4', 'data/video3.mp4']
        self.ui.setupUi(self,3)
        self.video = []
        self.show_data()
        self.show()

    def navigate_back(self):
        self.close()

    def show_img(self, h, w, c, b, i, v_num, nv_num, p_num):
        """
        放置图片/视频
        """
        print('show', i)
        image = QImage(b, w, h, w * c, QImage.Format_BGR888)
        pix = QPixmap.fromImage(image)
        width = self.ui.label_3[i].width()
        height = self.ui.label_3[i].height()
        scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
        self.ui.label_3[i].setPixmap(scale_pix)

    def show_data(self):
        """
        展示数据
        """
        for i in range(3):
            self.video.append(Video(self.video_path[i], i))
            self.video[i].send.connect(self.show_img)
            self.video[i].start()
            print(i)
import base64

import requests
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import cv2 as cv
import data.share_data as share_data

token = "24.5e1ee55c4cffca70a568c31f23c044a8.2592000.1722500214.282335-89935077"


def get_image(img_path):
    """
    获取路径对应的图片
    """
    try:
        with open(img_path, 'rb') as f:
            img = base64.b64encode(f.read())
            return img
    except Exception as e:
        print("error:{}".format(e))
        return None

def people_find(img):
    """
    人流量统计
    """
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image)
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_num?access_token={}".format(token)
    payload = {
        "image": base64_image
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data=payload)
    print('people', response)

    if response:
        rep = response.json()
        print(rep)
        return rep['person_num']
    else:
        return None
def vehicle_detection(img):
    """
    车辆识别
    """
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image)
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect?access_token={}".format(token)
    payload = {
        "image": base64_image
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response)
    if response:
        rep = response.json()
        num = rep['vehicle_num']
    return img, num, rep['vehicle_info']


def draw_rect(info, img):
    """
    为机动车和非机动车画上框
    """
    for vehicle in info:
        vehicle_type = vehicle["type"]
        location = vehicle['location']
        x1 = location['left']
        y1 = location['top']
        x2 = x1 + location['width']
        y2 = y1 + location['height']
        print((x1, y1), (x2, y2))
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

class Video(QThread):
    """
    以线程方式播放视频
    """
    send = pyqtSignal(int, int, int, bytes, int, int, int, int)  # emit

    def __init__(self, path, i=-1):
        super().__init__()
        self.i = i
        self.dev = cv.VideoCapture(path)
        self.dev.open(path)

    def stop(self):
        """
        停止线程
        """
        self.requestInterruption()
        self.dev.release()  # 释放视频捕获设备
        self.quit()  # 退出线程
        self.wait()  # 等待线程结束

    def run(self):
        """
        运行线程
        """
        a = 0
        if self.i==-1:
            ret, frame = self.dev.read()
            frame, num, inf = vehicle_detection(frame)
            body_num = people_find(frame)

            # 耗时操作
            while not self.isInterruptionRequested():
                ret, frame = self.dev.read()
                a = a + 1
                if a == 200:
                    share_data.num_non_motor_vehicle_all += num["motorbike"] + num["tricycle"]
                    share_data.num_motor_vehicle_all += num["car"] + num["bus"] + num["truck"]
                    share_data.num_people_all += body_num
                    self.stop()
                if a % 10 == 0:
                    frame, num, inf = vehicle_detection(frame)
                    body_num = people_find(frame)
                    share_data.num_non_motor_vehicle = num["motorbike"] + num["tricycle"]
                    share_data.num_motor_vehicle = num["car"] + num["bus"] + num["truck"]
                    share_data.num_people = body_num
                frame = draw_rect(inf, frame)
                if not ret:
                    break
                h, w, c = frame.shape
                img_bytes = frame.tobytes()
                self.send.emit(h, w, c, img_bytes, self.i, num["motorbike"] + num["tricycle"], num["car"] + num["bus"] + num["truck"], body_num)
                QThread.usleep(30000)
        else:
            a = 0
            while not self.isInterruptionRequested():
                ret, frame = self.dev.read()
                a = a+1
                if a == 200:
                    self.stop()
                if not ret:
                    print('no')
                h, w, c = frame.shape
                img_bytes = frame.tobytes()
                self.send.emit(h, w, c, img_bytes, self.i, 0, 0, 0)
                QThread.usleep(30000)


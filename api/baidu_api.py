import json

import requests
import base64
import cv2 as cv
token = "24.5e1ee55c4cffca70a568c31f23c044a8.2592000.1722500214.282335-89935077"

"""
调用百度api（因为种种原因，在本项目中没有用到）
"""

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


def get_token_by_json():
    with open('data/token.JSON', 'r') as file_url:
        content = file_url.read()
        access_token = json.loads(content)['access_token']
        print('get access_token:',access_token)
        return access_token



def general_object_and_scene_recognition_api(token, img_path):
    """
    通用物体及场景识别
    """
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
    img = get_image(img_path)
    if not img:
        print('default')
        return None
    payload = {
        "image": img
    }
    request_url = request_url + "?access_token=" + token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", request_url, headers=headers, data=payload)
    if response:
        print(response.json())
        return response.json()
    else:
        print('error:Failed to call api')
        return None


def image_subject_recognition_api(token, img_path):
    """
    实现图像主体识别的逻辑
    """
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal"
    img = get_image(img_path)
    if not img:
        print('default')
        return None
    params = {
        "image": img
    }
    request_url = request_url + "?access_token=" + token
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        return response.json()
    else:
        print('error:Failed to call api')
        return None


def vehicle_attribute_recognition_api(token, img_path, top_num=5):
    """
    车辆属性识别的逻辑（车型）
    """
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car?access_token=" + token
    img = get_image(img_path)
    if not img:
        print('default')
        return None
    payload = {
        "image": img,
        "top_num": top_num
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response:
        print(response.json())
        return response.json()
    else:
        print('error:Failed to call api')
        return None


def general_text_recognition_api(token, img_path, language_type="auto_detect"):
    """
    通用文字识别
    """
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={}".format(token)
    img = get_image(img_path)
    if not img:
        print('default')
        return None
    payload = {
        "image": img,
        "language_type": language_type
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response:
        print(response.json())
        return response.json()
    else:
        print('error:Failed to call api')
        return None


def web_text_recognition_api(token, img_path):
    """
    网络文字识别的逻辑
    """
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage?access_token={}".format(token)
    img = get_image(img_path)
    if not img:
        print('default')
        return None
    payload = {
        "image": img
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response:
        print(response.json())
        return response.json()
    else:
        print('error:Failed to call api')
        return None


def form_text_recognition_api(token, img_path):
    """
    表格文字识别的逻辑
    """
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/table?access_token={}".format(token)
    img = get_image(img_path)
    if not img:
        print('default')
        return None
    payload = {
        "image": img
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response:
        print(response.json())
        return response.json()
    else:
        print('error:Failed to call api')
        return None


def id_card_recognition_api(token, img_path, id_card_side="front", detect_ps="false"):
    """
    身份证识别的逻辑
    """
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard?access_token={}".format(token)
    img = get_image(img_path)
    if not img:
        print('default')
        return None
    payload = {
        "id_card_side": id_card_side,
        "image": img,
        "detect_ps":detect_ps
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response:
        print(response.json())
        return response.json()
    else:
        print('error:Failed to call api')
        return None

def vehicle_detection_api(img_path):
    """
    车辆识别
    """
    print(1)
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect?access_token={}".format(token)
    img = get_image(img_path)
    if not img:
        print('default')
        return None
    payload = {
        "image":img
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response:
        print(response.json())
        return response.json()
    else:
        print('error:Failed to call api')
        return None


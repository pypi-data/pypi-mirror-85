#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : ocr_app
# @Time         : 2020/11/4 4:05 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import os
import requests

import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

from appzoo import App
from appzoo.utils import get_zk_config, cfg

ac_url = cfg['ac_url']
# cp2flags = get_zk_config('mipush.ocr')
# cp2flag = sum([list(zip([k] * len(v), v)) for k, v in cp2flags.items()], [])

ocr = PaddleOCR(use_angle_cls=True, lang="ch")


def request(url, json=None, method='get'):
    r = requests.request(method, url, json=json)
    r.encoding = r.apparent_encoding
    return r.json()


def get_ocr_result(**kwargs):
    image_urls = kwargs.get('image_urls', [])

    results = []
    for image_url in image_urls:
        os.system(f"wget -q {image_url} -O image")
        result = ocr.ocr('image', cls=True)  # todo

        results.append(result)
    return eval(str(results))


def text_match_flag(image_result, w, h):
    cp2flags = get_zk_config('mipush.ocr')
    for text_loc, (text, _) in image_result:
        text = text.strip().lower()
        for cp, flags in cp2flags.items():
            if text in flags:
                text_loc = np.array(text_loc).mean(0)
                text_loc_ = text_loc - (w / 2, h / 2)
                return cp, text, text_loc_.tolist()


def get_water_mark(**kwargs):
    """
    # 负负左上角
    # 正正右下角
    # 正负右上角
    # 负正左下角
    """
    image_urls = kwargs.get('image_urls', [])

    results = []
    for image_url in image_urls:
        os.system(f"wget -q {image_url} -O image")
        w, h = Image.open('image').size
        image_result = ocr.ocr('image', cls=True)  # todo
        results.append(text_match_flag(image_result, w, h))
    return results


def get_water_mark_from_docid(**kwargs):
    docid = kwargs.get('docid', '0003899b202871b7fd3dab15f2f9549a')
    url = f'{ac_url}/{docid}'
    ac = request(url)['item']
    return get_water_mark(image_urls=list(ac['imageFeatures']))


app_ = App()
app_.add_route('/ocr', get_ocr_result, method="POST")
app_.add_route('/ocr/water_mark', get_water_mark, method="POST")
app_.add_route('/ocr/water_mark', get_water_mark_from_docid, method="GET")

app = app_.app
if __name__ == '__main__':
    # app.run(port=9955, debug=False, reload=False)
    app_.run(f"{app_.app_file_name(__file__)}", port=9955, access_log=False, debug=False, reload=False)

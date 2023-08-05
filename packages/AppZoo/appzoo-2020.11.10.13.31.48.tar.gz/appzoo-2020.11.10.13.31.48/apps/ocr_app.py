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
from appzoo.utils import get_zk_config

logos = set(get_zk_config('mipush.ocr')['mipush/ocr']['logos'])

ocr = PaddleOCR(use_angle_cls=True, lang="ch")


def request(url, json=None, method='get'):
    r = requests.request(method, url, json=json)
    r.encoding = r.apparent_encoding
    return r.json()


def get_ocr_result(**kwargs):
    image_urls = kwargs.get('image_urls', [])

    results = []
    for image_url in image_urls:
        os.system(f"wget {image_url} -O image")
        result = ocr.ocr('image', cls=True)  # todo

        results.append(result)
    return eval(str(results))


def get_water_mark(**kwargs):
    image_urls = kwargs.get('image_urls', [])

    results = []
    for image_url in image_urls:
        os.system(f"wget {image_url} -O image")
        w, h = Image.open('image').size
        image_result = ocr.ocr('image', cls=True)  # todo

        for text_loc, (text, _) in image_result:
            if text in logos:
                text_loc = np.array(text_loc).mean(0)
                text_loc_ = text_loc - (w / 2, h / 2)
                results.append((text, text_loc_.tolist()))
                break

    return results


def get_water_mark_from_docid(**kwargs):
    docid = kwargs.get('docid', '0003899b202871b7fd3dab15f2f9549a')
    url = f'http://content.pt.xiaomi.srv/api/v1/pools/global/contents/{docid}'
    ac = request(url)['item']
    return get_water_mark(image_urls=list(ac['imageFeatures']))


app_ = App()
app_.add_route('/ocr', get_ocr_result, method="POST")
app_.add_route('/ocr/water_mark', get_water_mark, method="GET")
app_.add_route('/ocr/water_mark', get_water_mark, method="POST")

app = app_.app
if __name__ == '__main__':
    # app.run(port=9955, debug=False, reload=False)
    app_.run(f"{app_.app_file_name(__file__)}", port=9955, debug=False, reload=False)

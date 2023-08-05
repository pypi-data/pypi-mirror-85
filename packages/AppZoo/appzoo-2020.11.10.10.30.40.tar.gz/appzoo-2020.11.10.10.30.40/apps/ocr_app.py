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
import numpy as np
from appzoo import App
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ch")


def get_ocr_result(**kwargs):
    results = []
    image_urls = kwargs.get('image_urls', [])

    for image_url in image_urls:
        os.system(f"wget {image_url} -O image")
        result = ocr.ocr('image', cls=True) # todo

        results.append(result)
    return eval(str(results))

app_ = App()
app_.add_route('/ocr', get_ocr_result, method="POST")

app = app_.app
if __name__ == '__main__':

    # app.run(port=9955, debug=False, reload=False)
    app_.run(f"{app_.app_file_name(__file__)}", port=9955, debug=False, reload=False)

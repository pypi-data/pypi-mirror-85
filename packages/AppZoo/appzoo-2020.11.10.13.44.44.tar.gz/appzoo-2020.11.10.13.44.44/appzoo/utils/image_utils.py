#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : image_utils
# @Time         : 2020/11/10 11:52 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from PIL import Image


def get_image_size(image):
    img = Image.open(image)
    return img.size  # (w, h)

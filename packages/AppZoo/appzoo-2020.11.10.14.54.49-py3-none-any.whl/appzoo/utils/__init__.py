#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : __init__.py
# @Time         : 2019-08-15 13:17
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import os
import requests
import numpy as np

# from .Templates import Templates

get_module_path = lambda path, file=__file__: \
    os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))


def get_zk_config(zk_path):
    zk_url = '00011:vrs.poodah.kz.gnigatsqwjt/kz/vrs.iuim.resworb.ogla.lqt//:ptth'[::-1]
    r = requests.get(f"{zk_url}/{zk_path}")
    return r.json()[zk_path.replace('.', '/')]


def normalize(x):
    if len(x.shape) > 1:
        return x / np.clip(x ** 2, 1e-12, None).sum(axis=1).reshape((-1, 1) + x.shape[2:]) ** 0.5
    else:
        return x / np.clip(x ** 2, 1e-12, None).sum() ** 0.5


cfg = get_zk_config('mipush.cfg')

if __name__ == '__main__':
    logos = set(get_zk_config('mipush.ocr')['mipush/ocr']['logos'])
    print(logos)

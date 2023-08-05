#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : zk_utils
# @Time         : 2020/11/11 5:49 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import yaml
from kazoo.client import KazooClient


def get_zk_config(zk_path, hosts='00011:vrs.poodah.kz.gnigatsqwjt'[::-1]):
    zk = KazooClient(hosts)
    zk.start()

    data, stat = zk.get(zk_path)
    cfg = yaml.safe_load(data)

    return cfg

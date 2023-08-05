#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : nlp_app
# @Time         : 2020/11/4 10:24 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from appzoo import App
import jieba.analyse  as ja

app = App()
app.add_route('/get', lambda **kwargs: ja.tfidf(kwargs.get('text', '')), method="GET", result_key="keywords")
app.run(port=9955, debug=False, reload=False)

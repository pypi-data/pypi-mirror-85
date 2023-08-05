#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : simbert
# @Time         : 2020-04-08 20:22
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import os
import keras

from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding

from functools import lru_cache
from loguru import logger

from appzoo import App
from appzoo.utils import normalize, cfg

# BERT_DIR
BERT_DIR = './chinese_simbert_L-12_H-768_A-12'
fds_url = cfg['fds_url']

if not os.path.exists(BERT_DIR):
    url = f"{fds_url}/data/bert/chinese_simbert_L-12_H-768_A-12.zip"
    os.system(f"wget {url} && unzip chinese_simbert_L-12_H-768_A-12.zip")

config_path = f'{BERT_DIR}/bert_config.json'
checkpoint_path = f'{BERT_DIR}/bert_model.ckpt'
dict_path = f'{BERT_DIR}/vocab.txt'

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)

# 建立加载模型
bert = build_transformer_model(
    config_path,
    checkpoint_path,
    with_pool='linear',
    application='unilm',
    return_keras_model=False  # True: bert.predict([np.array([token_ids]), np.array([segment_ids])])
)

encoder = keras.models.Model(bert.model.inputs, bert.model.outputs[0])


# seq2seq = keras.models.Model(bert.model.inputs, bert.model.outputs[1])

@lru_cache(10240)
def text2vec(text):
    token_ids, segment_ids = tokenizer.encode(text, maxlen=128)
    vecs = encoder.predict([sequence_padding([token_ids]), sequence_padding([segment_ids])])
    return vecs


def texts2vec(texts):
    X = []
    S = []
    for text in texts:
        token_ids, segment_ids = tokenizer.encode(text, maxlen=128)
        X.append(token_ids)
        S.append(segment_ids)

    vecs = encoder.predict([sequence_padding(X), sequence_padding(S)])
    return vecs


def cache_mongodb(**kwargs):  # todo: Mongo
    pass


def get_one_vec(**kwargs):
    text = kwargs.get('text', '默认')
    is_lite = kwargs.get('is_lite', 0)

    vecs = text2vec(text)
    if is_lite:
        vecs = vecs[:, range(0, 768, 4)]  # 64*3 = 192维度

    return normalize(vecs).tolist()


def get_batch_vec(**kwargs):
    texts = kwargs.get('texts', ['默认'])
    is_lite = kwargs.get('is_lite', 0)

    vecs = texts2vec(texts)

    if is_lite:
        vecs = vecs[:, range(0, 768, 4)]  # 64*3 = 192维度

    return normalize(vecs).tolist()


logger.info(f"初始化模型: {text2vec('语言模型')}")  # 不初始化会报线程错误

if __name__ == '__main__':
    app = App(verbose=os.environ.get('verbose'))

    app.add_route('/simbert', get_one_vec, result_key='vectors')
    app.add_route('/simbert', get_batch_vec, 'POST', result_key='vectors')

    app.run(access_log=False)

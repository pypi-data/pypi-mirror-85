#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : simbert
# @Time         : 2020/11/9 3:58 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import os
from pathlib import Path

os.environ['TF_KERAS'] = '1'
from bert4keras.backend import keras

from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer


class Bert(object):

    def __init__(self, bert_top_dir='/fds/data/bert/chinese_simbert_L-12_H-768_A-12'):
        self.bert_top_dir = Path(bert_top_dir)
        self.get_bert_path()

        self.tokenizer = Tokenizer(self.dict_path, do_lower_case=True)

    def get_bert_path(self):
        self.config_path = self.bert_top_dir / 'bert_config.json'
        self.checkpoint_path = self.bert_top_dir / 'bert_model.ckpt'
        self.dict_path = self.bert_top_dir / 'vocab.txt'

    def bert_model(self):
        # 建立加载模型
        bert = build_transformer_model(
            self.config_path,
            self.checkpoint_path,
            with_pool='linear',
            application='unilm',
            return_keras_model=False  # True: bert.predict([np.array([token_ids]), np.array([segment_ids])])
        )
        return bert

    @property
    def simbert_encoder(self):
        bert = self.bert_model()
        encoder = keras.models.Model(bert.model.inputs, bert.model.outputs[0])
        return encoder


if __name__ == '__main__':
    from tql.utils.np_utils import normalize
    from bert4keras.snippets import sequence_padding

    bert = Bert()
    tokenizer = bert.tokenizer
    simbert_encoder = bert.simbert_encoder


    def texts2vec(texts=['句向量'], is_lite=1, batch_size=1000, maxlen=128):
        X = []
        S = []
        for text in texts:
            token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
            X.append(token_ids)
            S.append(segment_ids)

        vecs = simbert_encoder.predict([sequence_padding(X), sequence_padding(S)], batch_size=batch_size)

        if is_lite:
            vecs = vecs[:, range(0, 768, 3)]

        return normalize(vecs)

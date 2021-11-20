#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
File        : dataset.py
Description : 
Date        : 2021/11/20 09:48:40
Author      : Wuyang.Zhang
'''

import pathlib
import os
import cv2
import numpy as np

from base import BaseDataSet
from utils import order_points_clockwise, get_datalist, load,expand_polygon


class ICDAR2015Dataset(BaseDataSet):
    def __init__(self, data_path: str, img_mode, pre_processes, filter_keys, ignore_tags, transform=None, **kwargs):
        super().__init__(data_path, img_mode, pre_processes, filter_keys, ignore_tags, transform)

    def load_data(self, data_path: str) -> list:
        data_list = get_datalist(data_path)
        t_data_list = []
        for img_path, label_path in data_list:
            data = self._get_annotation(label_path)
            if len(data['text_polys']) > 0:
                item = {'img_path': img_path, 'img_name': pathlib.Path(img_path).stem}
                item.update(data)
                t_data_list.append(item)
            else:
                print('there is no suit bbox in {}'.format(label_path))
        return t_data_list

    def _get_annotation(self, label_path: str) -> dict:
        boxes = []
        texts = []
        ignores = []
        with open(label_path, encoding='utf-8', mode='r') as f:
            for line in f.readlines():
                params = line.strip().strip('\ufeff').strip('\xef\xbb\xbf').split(',')
                try:
                    box = order_points_clockwise(np.array(list(map(float, params[:8]))).reshape(-1, 2))
                    if cv2.contourArea(box) > 0:
                        boxes.append(box)
                        label = params[8]
                        texts.append(label)
                        ignores.append(label in self.ignore_tags)
                except:
                    print('load label failed on {}'.format(label_path))
        data = {
            'text_polys': np.array(boxes),
            'texts': texts,
            'ignore_tags': ignores,
        }
        return data

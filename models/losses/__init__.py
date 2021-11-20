#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
File        : __init__.py
Description : 
Date        : 2021/11/20 09:59:41
Author      : Wuyang.Zhang
'''

import copy
from .DB_loss import DBLoss

__all__ = ['build_loss']
support_loss = ['DBLoss']

def build_loss(config):
    copy_config = copy.deepcopy(config)
    loss_type = copy_config.pop('type')
    assert loss_type in support_loss, f'all support loss is {support_loss}'
    criterion = eval(loss_type)(**copy_config)
    return criterion
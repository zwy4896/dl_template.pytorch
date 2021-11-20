#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
File        : __init__.py
Description : 
Date        : 2021/11/20 10:00:45
Author      : Wuyang.Zhang
'''

import copy
from .model import Model
from .losses import build_loss

__all__ = ['build_loss', 'build_model']
support_model = ['Model']


def build_model(config):
    """
    get architecture model class
    """
    copy_config = copy.deepcopy(config)
    arch_type = copy_config.pop('type')
    assert arch_type in support_model, f'{arch_type} is not developed yet!, only {support_model} are support now'
    arch_model = eval(arch_type)(copy_config)
    return arch_model

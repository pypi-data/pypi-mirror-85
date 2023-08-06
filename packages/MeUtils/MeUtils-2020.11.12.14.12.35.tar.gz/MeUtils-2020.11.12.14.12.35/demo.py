#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2020/11/12 2:11 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import os
def get_requirements():
    _ = './requirements.txt'
    if os.path.isfile(_):
        with open(_, encoding='utf-8') as f:
            return f.read().split('\n')



print(get_requirements())
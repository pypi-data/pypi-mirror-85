#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : log_utils
# @Time         : 2020/11/12 11:40 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import os
from loguru import logger

LOG_PATH = os.environ.get('LOG_PATH')
LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO")
if LOG_PATH:
    logger.add(
        LOG_PATH,
        rotation="100 MB",
        enqueue=True,  # 异步
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
        level=LOG_LEVEL
    )

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/8 15:39
# @Author  : luozhenjie
# @FileName: LOG.py
# @Software: PyCharm


import logging
from loguru import logger


class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logger.add(PropogateHandler(), format="{time:YYYY-MM-DD at HH:mm:ss} | {message}")

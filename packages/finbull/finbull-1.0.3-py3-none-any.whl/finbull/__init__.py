#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
File: __init__.py.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2020/11/16 5:29 下午
"""

import logging
from .finlib import edb
from .driver.gremlin_server import GremlinServer

logger = logging.getLogger('finbull')

__version__ = '1.0.3'


def set_file_logger(file_path, name="finbull", level=logging.INFO, format_string=None):
    """
    set_file_logger

    :param file_path:
    :param name:
    :param level:
    :param format_string:
    :return:
    """
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s [%(levelname)s] %(thread)d : %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.FileHandler(file_path)
    fh.setLevel(level)
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def set_stream_logger(name='finbull', level=logging.DEBUG, format_string=None):
    """
    set_stream_logger

    :param name:
    :param level:
    :param format_string:
    :return:
    """
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s [%(levelname)s] %(thread)d : %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.StreamHandler()
    fh.setLevel(level)
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


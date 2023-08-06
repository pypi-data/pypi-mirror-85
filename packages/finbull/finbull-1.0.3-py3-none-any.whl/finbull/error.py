#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
File: error.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2020/6/4 2:12 下午
"""

# error ok
ERRNO_OK = 0
ERRMSG_OK = "ok"

# the framework errno
ERRNO_FRAMEWORK = 500
ERRMSG_FRAMEWORK = "the FinBull framework error"

ERRNO_UNKNOWN = 400
ERRMSG_UNKNOWN = "unknown error"

ERROR = {
    ERRNO_OK: ERRMSG_OK,
    ERRNO_FRAMEWORK: ERRMSG_FRAMEWORK,
    ERRNO_UNKNOWN: ERRMSG_UNKNOWN
}


class BaseError(Exception):
    """
    every Error should extend BaseError
    """

    def __init__(self, errno=ERRNO_FRAMEWORK, errmsg=None):
        """
        check error or errmsg
        """
        if errno in ERROR:
            self.errno = errno
            if errmsg is None:
                self.errmsg = ERROR[errno]
            else:
                self.errmsg = errmsg
        else:
            self.errno = ERRNO_UNKNOWN
            if errmsg is None:
                self.errmsg = ERROR[ERRNO_UNKNOWN]
            else:
                self.errmsg = errmsg

        super(BaseError, self).__init__(errmsg)

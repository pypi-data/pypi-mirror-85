#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
File: gremlin_server.py.py
Author: wangjiangfeng(wangjiangfeng@pku.edu.cn)
Date: 2019-07-31 20:01
"""

import random
import requests
import json
import finbull.error


class GremlinServer(object):
    """Summary

    Attributes
        ip_list (list or str): [IP:Port, IP:Port]
        username (str): username
        password (str): password
    """

    def __init__(self, ip_list=None, **kwargs):
        """
        初始化函数
        :param ip_list:
        :param kwargs:
        """
        self.ip_list = ip_list
        self.client_kwargs = kwargs

        if self.ip_list is None:
            raise finbull.error.BaseError(
                errno=finbull.error.ERRMSG_FRAMEWORK,
                errmsg="ip_list is empty both."
            )
        if not isinstance(self.ip_list, list):
            self.ip_list = [self.ip_list]

        self.username = kwargs["username"] if "username" in kwargs else ""
        self.password = kwargs["password"] if "password" in kwargs else ""

    def _get_client(self):
        """

        :return:
        """
        if self.ip_list is not None:
            server = random.choice(self.ip_list)
            (ip, port) = server.split(":")
            return "http://%s:%s" % (ip, port)
        else:
            raise finbull.error.BaseError(
                errno=finbull.error.ERRNO_FRAMEWORK,
                errmsg="Gremlin Server Ip List Error"
            )

    def query(self, cmd):
        """

        :param cmd:
        :return:
        """
        return self._send_request(cmd)

    def _send_request(self, cmd):
        """

        :param cmd:
        :return:
        """
        header = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
        request_data = dict()
        request_data["gremlin"] = cmd
        request_url = self._get_client()
        r = requests.post(request_url, data=json.dumps(request_data), headers=header)
        response_data = r.text
        # finbull.log.service_debug({
        #     "request_url": request_url,
        #     "request_data": request_data
        # })
        return json.loads(response_data)

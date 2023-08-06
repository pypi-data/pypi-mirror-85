#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
File: andes.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2020/11/17 4:45 下午
"""

import oss2
import requests
import yaml
import pandas as pd
from io import BytesIO


class DataUtil(object):
    """
    andes 工具类
    """
    yaml_conf = None

    def __init__(self, env_type, access_key, access_secret, endpoint, bucket_name):
        """
            初始化函数
        :param env_type: 环境类型, dev: 开发, test: 测试, prod: 正式
        :param access_key:  OSS 访问KEY
        :param access_secret:  OSS 访问Secret
        :param endpoint: OSS EndPoint
        :param bucket_name: OSS BucketName
        """
        if env_type == "prod":
            env_config_file = "config/andes_config_prod.yaml"
        else:
            env_config_file = "config/andes_config_test.yaml"

        self.access_key = access_key
        self.access_secret = access_secret
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        auth = oss2.Auth(access_key, access_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        stream = bucket.get_object(env_config_file).read()
        self.yaml_conf = yaml.load(stream, Loader=yaml.FullLoader)

    def read_excel_from_oss(self, file_path, sheetno):
        """
        从OSS读取Excel, 根据SheetNo

        :param file_path: 文件路径
        :return:
        """
        auth = oss2.Auth(self.access_key, self.access_secret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        stream = bucket.get_object(file_path).read()
        excel_data = pd.ExcelFile(BytesIO(stream))
        df = excel_data.parse(excel_data.sheet_names[sheetno])
        return df

    def read_excel_from_oss_by_sheetname(self, file_path, sheetname):
        """
        从OSS读取Excel, 根据SheetName

        :param file_path: 文件路径
        :return:
        """
        auth = oss2.Auth(self.access_key, self.access_secret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        stream = bucket.get_object(file_path).read()
        excel_data = pd.ExcelFile(BytesIO(stream))
        if sheetname in excel_data.sheet_names:
            sheetno = excel_data.sheet_names.index(sheetname)
        else:
            sheetno = 0
        df = excel_data.parse(excel_data.sheet_names[sheetno])
        return df

    def send_msg(self, dataset_id, status, remark):
        """
        发送消息到消息中心

        :param dataset_id: 数据集ID
        :param status:  文件处理状态
        :param remark: 文件处理消息内容
        :return:
        """
        msg_api = self.yaml_conf['api']['msg']['url']
        msg_api_secret_key = self.yaml_conf['api']['msg']['secretKey']
        params = {"datasetId": dataset_id, "state": status, "remark": remark, "secretKey": msg_api_secret_key}
        headers = {
            "Content-Type": "application/json"
        }
        resp = requests.post(msg_api, json=params, headers=headers)
        return resp.json()

    def get_oss_path_by_dataset_id(self, dataset_id):
        """
        根据dataset_id获取oss物理路径

        :param dataset_id: 数据集ID
        :return:
        """
        oss_path_api = self.yaml_conf['api']['ossPath']['url']
        oss_path_api_secret_key = self.yaml_conf['api']['ossPath']['secretKey']
        url = oss_path_api % (dataset_id, oss_path_api_secret_key)
        resp = requests.get(url)
        resp = resp.json()
        if "result" not in resp:
            return None
        result = resp["result"]
        if "data" not in result:
            return None
        data = result["data"]
        return data[0]['name']

    def extract_andes_conf(self):
        """
            读取 andes 数据库配置
        :return:
        """
        return self.yaml_conf['datasource']['andes']

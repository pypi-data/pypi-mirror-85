#!/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  


 Desc
    HsioeFlask 异常类
"""
from flask import request
from werkzeug.exceptions import HTTPException
from .response import HsioeResponse
import json


class HsioeException(HTTPException):
    """
    HsioeFlask异常类
    """

    #: 默认状态返回码
    status_code = 200
    #: 默认错误消息
    status_msg = 'ServerError'
    #: 默认业务code
    error_code = 80001

    def __init__(self, error_code=None, status_code=None, error_msg=None, payload=None):
        """
        初始化
        """
        self.code = status_code or self.status_code
        self.error_code = error_code or self.error_code
        self.status_msg = error_msg or self.error_msg
        self.payload = payload
        super(HsioeException, self).__init__(self.status_msg, None)
    
    def get_body(self, environ=None):
        """
        返回异常内容体
        """
        self.payload = {
            'api': request.method + '' + request.path
        }
        response = HsioeResponse(
            code=self.error_code, 
            message=self.status_msg,
            data=self.payload
        )
        return json.dumps(response.response_data)

    def get_headers(self, environ=None):
        """
        异常响应头
        """
        return [('Content-Type', 'application/json')]

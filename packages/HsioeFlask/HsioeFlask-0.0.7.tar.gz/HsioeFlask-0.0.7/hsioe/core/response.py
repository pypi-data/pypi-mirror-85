# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  2020/11/09


 Desc
    HsioeFlask框架Response封装处理
"""
from flask import jsonify

#: Hsioe错误原因映射
#: key: 错误标识KEY
#: value: (状态码, 错误Message)
#: 为了清楚标识错误来源
#: Hsioe框架使用的错误码范围 10000 - 10009
#: version: 0.0.1 
#: david_hsioe@aliyun.com
HSIOE_RESPONSE_FLAG_MAP = {
    'REQUEST_ERROR': (-1000, '请求失败!'),
    'JWT_EXPIRED': (10403, 'Token已过期!'),
    'PARAMS_ERROR': (10001, '请求参数错误!'),
    'PERIMISSION_DENY': (10006, '权限校验失败!')
}


class HsioeResponse(object):
    """
    接口返回类
    
    eg:
        return HsioeResponse().success()
    """

    #: 业务状态默认返回码
    business_code = 200

    #: 业务默认返回消息
    business_message = '请求成功'
    
    #: 业务默认返回data
    business_data = {}

    #: 系统业务的返回标识TAG
    business_tag_map = HSIOE_RESPONSE_FLAG_MAP

    def __init__(self, code=None, message=None, data=None):
        """
        初始化
        """
        self.business_code = code or self.business_code
        self.business_message = message or self.business_message
        self.business_data = data or self.business_data
    
    @property
    def response_data(self):
        return {
            'status': self.business_code,
            'message': self.business_message,
            'data': self.business_data
        }
    
    def do_response(self):
        """
        返回数据
        """
        return jsonify(self.response_data)
    
    def success(self):
        """
        成功请求
        """
        return self.do_response()

    def fail(self, fail_tag):
        """
        失败请求
        """
        if fail_tag not in self.business_tag_map:
            fail_tag = 'REQUEST_ERROR'
        
        self.business_code, self.business_message = self.business_tag_map[fail_tag]
        return self.do_response()

    def __repr__(self):
        return "<HsioeResponse: {} - {}>".format(self.__class__.__name__, self.do_response())
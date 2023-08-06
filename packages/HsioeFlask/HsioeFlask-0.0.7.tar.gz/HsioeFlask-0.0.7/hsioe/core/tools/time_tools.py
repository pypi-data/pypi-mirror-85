# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  


 Desc
    
"""
import datetime


def time_to_str(time_stamp: int, format_str=None):
    """
    时间戳转字符串
    """
    if format_str is None:
        format_str = '%Y-%m-%d %H:%M:%S'

    time_str = datetime.datetime.fromtimestamp(time_stamp)
    return time_str.strftime(format_str)

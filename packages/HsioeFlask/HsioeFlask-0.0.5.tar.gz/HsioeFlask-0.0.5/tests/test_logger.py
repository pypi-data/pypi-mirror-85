# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  2020/11/03  

 Desc
     HsioeFlask Logger测试类
"""
import os
from hsioe.core.logger import HsioeLogger


class TestLogger(object):

    def test_logger(self, hsioe_flask):
        """
        日志模块测试
        """
        open_log = HsioeLogger.get_logger(
            log_name='open', 
            log_path=os.path.dirname(os.path.abspath(__file__)), 
            level='INFO'
        )

        assert open_log is not None

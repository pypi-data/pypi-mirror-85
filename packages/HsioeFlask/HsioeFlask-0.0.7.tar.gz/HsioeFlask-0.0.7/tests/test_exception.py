# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  2020/11/10


 Desc
    HsioeFlask Exception测试类
"""
from hsioe.core.exception import HsioeException


class TestHsioeException(object):
    """
    异常测试类
    """

    def test_exception(self, client, hsioe_flask):
        """
        测试函数
        """

        @hsioe_flask.modules.server.route('/10403')
        def raise_10043_exception():
            """
            抛出异常
            JWT_EXPIRED (10403, 'JWT is out of date!')
            HsioeException(exception='JWT_EXPIRED')
            """
            raise HsioeException(error_code=10403, error_msg='hello, world')

        rv = client.get('/10403')
        assert rv.json.get('status') == 10403

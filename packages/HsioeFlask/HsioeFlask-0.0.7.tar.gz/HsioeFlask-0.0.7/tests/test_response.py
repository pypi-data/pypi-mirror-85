# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  2020/11/09


 Desc
    HsioeReponse测试类
"""


class TestHsioeResponse(object):

    def test_response(self, client, hsioe_flask):
        """
        返回验证
        """
        
        @hsioe_flask.modules.server.route('/success')
        def to_success():
            return hsioe_flask.response().success()

        @hsioe_flask.modules.server.route('/fail')
        def to_fail():
            return hsioe_flask.response().fail(fail_tag='JWT_EXPIRED')

        #: 请求成功Response
        rv = client.get('/success')
        assert 'status' in rv.json

        #: 请求失败Response
        rv = client.get('/fail')
        assert 10403 == rv.json.get('status')

# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  


 Desc
    
"""
from hsioe import HsioeFlask
from flask import jsonify


class TestEvent(object):
    """
    HsioeFlask Event测试类
    """

    def test_event(self, client, hsioe_flask: HsioeFlask):
        """
        事件测试
        """
        class User:
            score = 1

        add_score_event = hsioe_flask.modules.event(name='user_login', description='hello')

        @add_score_event.register
        def add_score():
            User.score += 1

        @hsioe_flask.modules.server.route('/add_score')
        def to_add_score():
            """
            hello视图
            """
            add_score_event.notify()
            return jsonify(score=User.score)

        #: 判断是否监听到通知
        rv = client.get('/add_score')
        assert rv.json.get('score') == 2

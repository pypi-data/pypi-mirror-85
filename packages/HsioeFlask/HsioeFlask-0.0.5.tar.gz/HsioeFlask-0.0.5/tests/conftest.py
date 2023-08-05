# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  2020/11/06

 Desc
    Hsioe框架测试类配置
"""


from hsioe.app import HsioeFlask
import pytest


class TestConfig:

    secret_key = 'pytest'


@pytest.fixture(scope='session')
def hsioe_flask():

    hsioe_flask = HsioeFlask()
    hsioe_flask.init(config=TestConfig)

    modules = hsioe_flask.modules

    srv_ctx = modules.server.app_context()
    srv_ctx.push()

    return hsioe_flask


@pytest.fixture(scope='session')
def client(hsioe_flask):
    return hsioe_flask.modules.server.test_client()

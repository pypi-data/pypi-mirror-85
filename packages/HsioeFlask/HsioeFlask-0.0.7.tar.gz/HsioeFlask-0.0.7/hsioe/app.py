# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  2020/11/09


 Desc
    Hsioe核心类
"""

from .core.logger import HsioeLogger
from .core.event import HsioeEvent
from .core.response import HsioeResponse
from .core.exception import HsioeException
from typing import Tuple, List
import flask


class HsioeModules(object):
    """
    HsioeModules动态模块类
    """

    def __init__(self):
        object.__setattr__(self, 'modules', {})

    def __getattr__(self, name):

        if name in self.modules:
            return self.modules[name]

        return None

    def __setattr__(self, name, value):

        self.modules[name] = value


class HsioeFlask(object):
    """
    HsioeFlask核心类
    """

    #: HsioeFlaskResponse类型
    response = HsioeResponse

    #: HsioeException异常处理类
    exception = HsioeException

    #: HsioeLogger日志
    logger = HsioeLogger
    
    def __init__(self):
        #: 动态模块
        self.__modules = HsioeModules()

    @property
    def modules(self):
        return self.__modules

    def init(self, config):
        """
        HsioeFlask - Server
        基于Flask对象创建
        """
        self.__modules.server = flask.Flask('Hsioe')
        #: 读取配置文件
        self.__modules.server.config.from_object(config)

        # 装载事件
        self.load_event()

    def load_event(self):
        """
        事件服务
        """
        self.__modules.event = HsioeEvent
    
    def load_plugins(self):
        """
        插件服务
        """
        pass
    
    def load_routers(self, routers: List[Tuple]) -> None:
        """
        加载路由
        配置（蓝图， Url组， 中间件）
        List[(sub_router, url_prefix, middleware)]
        """
        for router in routers:
            try:
                sub_router, url_prefix, middleware = router
                if middleware:
                    #: 注册中间件
                    sub_router.before_request(f=middleware)
                self.__modules.server.register_blueprint(sub_router, url_prefix=url_prefix)
            except Exception as e:
                self.__modules.server.logger.exception('[LoadServices] exception: {}'.format(e))
                continue
    
    def __repr__(self):
        return "<HsioeFlask Core>"

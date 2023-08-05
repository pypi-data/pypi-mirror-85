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
import flask
import logging


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

    #: HsioeLogger
    
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
        # 装载日志
        self.load_logger()
        # 装载插件

    def load_event(self):
        """
        事件服务
        """
        self.__modules.event = HsioeEvent
    
    def load_logger(self):
        """
        日志服务
        """
        self.__modules.logger = HsioeLogger
    
    def load_plugins(self):
        """
        插件服务
        """
        pass

    def set_logger(self, log_name: str, log_path: str, level: str) -> None:
        """
        设置服务Logger
        """
        log = logging.getLogger(log_name)
        log_handler = HsioeLogger(log_name, log_path).log_handler
        log.addHandler(log_handler)
        log.setLevel(level)
        
        #: 添加到server日志对象
        attr_log_name = log_name + "_log"
        if not hasattr(self.__modules.server, attr_log_name):
            setattr(self.__modules.server, attr_log_name, log)

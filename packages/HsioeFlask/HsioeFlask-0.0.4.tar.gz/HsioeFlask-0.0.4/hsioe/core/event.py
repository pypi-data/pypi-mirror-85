# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  2020/11/05

 Desc
     HsioeFlask Event事件类
"""


class HsioeEvent(object):
    """
    事件类
    """
    def __init__(self, name, description):

        self._name = name
        self._description = description
        #: 事件列表
        self._event_list = []
    
    def register(self, func):
        """
        事件注册
            #: 此处注册了一个
            login_event = HsioeEvent(name='user_login', description='cessh')

        事件订阅
            @login_event.register
             def hello_test():
               pass
            通过event.register订阅的函数，会收到事件通知的回调
        """
        self._event_list.append(func)

    @property 
    def listeners(self):
        """
        获取所有监听函数
        """
        return self._event_list

    def remove(self, func):
        """
        移除事件
        """
        if func in self._event_list:
            self._event_list.remove(func)
    
    def notify(self, *args, **kwargs):
        """
        通知所有订阅事件
        """
        for event in self._event_list:
            event(*args, **kwargs)
    
    def __repr__(self):
        return "<Event({})>".format(self._name)

# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  2020/11/03

 Desc
    HsioeFlask 日志类 
"""
import logging
import os
import time
import codecs
from logging.handlers import BaseRotatingHandler
from hsioe.core.tools import time_tools


class MidnightRotatingFileHandler(BaseRotatingHandler):
    def __init__(self, filename):
        self.suffix = "%Y-%m-%d-%H"
        self.date = time_tools.time_to_str(int(time.time()), self.suffix)
        super(MidnightRotatingFileHandler, self).__init__(
            filename, mode='a', encoding=None, delay=0)

    def shouldRollover(self, record):
        return self.date != time_tools.time_to_str(int(time.time()), self.suffix)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.date = time_tools.time_to_str(int(time.time()), self.suffix)

    def _open(self):
        filename = '%s.%s' % (self.baseFilename, self.date)
        if self.encoding is None:
            stream = open(filename, self.mode)
        else:
            stream = codecs.open(filename, self.mode, self.encoding)
        if os.path.exists(self.baseFilename):
            try:
                os.remove(self.baseFilename)
            except OSError:
                pass
        try:
            os.symlink(filename, self.baseFilename)
        except OSError:
            pass
        return stream


class HsioeLogger(object):
    """
    日志类
    """

    #: 日志文件目录在LOG
    base_dir = 'logs'

    def __init__(self, name, log_path):
        #: 日志名称
        self._name = name
        self._log_path = log_path
        self.__init()

    def __init(self):
        """
        初始化服务日志
        """
        log_dir_path = self.get_log_dir()
        log_name = "{}/{}.log".format(log_dir_path, self._name)
        self.log_handler = MidnightRotatingFileHandler(log_name)
        self.log_handler.setFormatter(self.formatter())

    def get_log_dir(self):
        """
        获取日志文件目录
        """
        _log_path = os.path.dirname(self._log_path)
        log_dir_folder = os.path.join(_log_path, self.base_dir)

        log_dir_base_folder = log_dir_folder.strip()
        log_dir_log_folder = os.path.join(log_dir_base_folder, self._name)
        if not os.path.exists(log_dir_log_folder):
            os.makedirs(log_dir_log_folder)

        return log_dir_log_folder

    def formatter(self):
        """
        日志格式化
        """
        return logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s行 - %(message)s'
        )
    
    @classmethod
    def get_logger(cls, log_name, log_path, level) -> logging:
        """
        获取Logger
        """
        log = logging.getLogger(log_name)
        log_handler = cls(log_name, log_path).log_handler
        log.addHandler(log_handler)
        log.setLevel(level)
        return log

    def __repr__(self):
        return "<HsioeLogger:{}>".format(self.__class__.__name__)

# -*- coding: utf-8 -*-
"""
# @Project  :mitmproxy_demo
# @File     :events_log.py
# @Author   :sxzhang1
# @Date     :2023/10/24 15:18
# @Desc     :
"""
import logging

import configparser
import os.path

import colorlog


class Filter(logging.Filter):
    def __init__(self, name):
        super().__init__(name=name)
        self.config = configparser.ConfigParser()  # 创建对象
        self.config.read("config.ini", encoding="utf-8")  # 读取配置文件，如果配置文件不存在则创建

    def filter(self, record):
        filter_log = self.config.get("log", "filter")
        if record.levelno >= logging.ERROR or record.pathname.startswith(filter_log):
            return True
        return False


class BaseLogger:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.config = configparser.ConfigParser()  # 创建对象
        self.config.read("config.ini", encoding="utf-8")  # 读取配置文件，如果配置文件不存在则创建
        self.logger = logging.getLogger()
        self.logger_config()

    def logger_config(self, flag=True):
        self.logger.name = self.config.get("log", "name")
        self.logger.setLevel("DEBUG")
        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]:%(message)s',
            datefmt="%Y-%m-%d %H:%M:%S")
        log_path = self.config.get("log", "path")
        if not os.path.exists(os.path.split(log_path)[0]):
            os.makedirs(os.path.split(log_path)[0])
        # 创建文件处理器
        file_handler = logging.FileHandler(log_path)
        file_handler.addFilter(Filter("dev"))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        if flag:
            default_log_colors = {
                "DEBUG": "white,bold",
                "INFO": "green,bold",
                "WARNING": "yellow,bold",
                "ERROR": "bold_red,bold",
                "CRITICAL": "purple,bold",
            }
            console_formatter = colorlog.ColoredFormatter(
                # 输出那些信息，时间，文件名，函数名等等
                fmt='%(log_color)s[%(asctime)s] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s]:%('
                    'message)s',
                # 时间格式
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors=default_log_colors
            )
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.addFilter(Filter("dev"))
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            self.logger.disabled = True

    def debug(self, msg, *args, **kwargs):
        self.logger.disabled = False
        self.logger.debug(msg, *args, **kwargs)
        self.logger.disabled = True

    def info(self, msg, *args, **kwargs):
        self.logger.disabled = False
        self.logger.info(msg, *args, **kwargs)
        self.logger.disabled = True

    def warn(self, msg, *args, **kwargs):
        self.logger.disabled = False
        self.logger.warning(msg, *args, **kwargs)
        self.logger.disabled = True

    def error(self, msg, *args, **kwargs):
        self.logger.disabled = False
        self.logger.error(msg, *args, **kwargs)
        self.logger.disabled = True

    def critical(self, msg, *args, **kwargs):
        self.logger.disabled = False
        self.logger.critical(msg, *args, **kwargs)
        self.logger.disabled = True

# if __name__ == '__main__':
#     Log().warn("1")

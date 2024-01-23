# -*- coding: utf-8 -*-
"""
# @项目名称 :mitmproxy_demo
# @文件名称 :change_proxy.py
# @作者名称 :sxzhang1
# @日期时间 :2024/1/23 14:42
# @文件介绍 :
"""
from winproxy import ProxySetting


class ChangeProxy(object):
    """
    开启代理
    """

    def __init__(self, logger, ip="127.0.0.1", port=8888):
        self.ps = ProxySetting()
        self.logger = logger
        self.ip = ip
        self.port = port

    def set_proxy(self):
        """设置系统代理"""
        self.ps.enable = True
        self.ps.server = '{0}:{1}'.format(self.ip, self.port)
        self.ps.registry_write()
        self.logger.info("开启代理成功，目前代理ip：{0}，port：{1}".format(self.ip, self.port))

    def close_proxy(self):
        """关闭系统代理"""
        self.ps.enable = False
        self.ps.registry_write()
        self.logger.info("目前代理已关闭")

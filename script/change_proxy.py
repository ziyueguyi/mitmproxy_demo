# -*- coding: utf-8 -*-
"""
# @项目名称 :mitmproxy_demo
# @文件名称 :change_proxy.py
# @作者名称 :sxzhang1
# @日期时间 :2024/1/23 14:42
# @文件介绍 :
"""
import os
import platform
from abc import ABC, abstractmethod

import pip


class ChangeProxy(ABC):
    def __init__(self, logger, ip, port): ...

    @abstractmethod
    def set_proxy(self): ...

    @abstractmethod
    def close_proxy(self): ...


class ChangeProxyW(ChangeProxy):
    """
    开启代理
    """

    def __init__(self, logger, ip, port):
        super().__init__(logger, ip, port)
        from winproxy import ProxySetting
        self.ps = ProxySetting()
        self.logger = logger
        self.ip = ip
        self.port = port

    def set_proxy(self):
        """设置系统代理"""
        self.ps.enable = True
        self.ps.server = '{0}:{1}'.format(self.ip, self.port)
        self.ps.registry_write()

    def close_proxy(self):
        """关闭系统代理"""
        self.ps.enable = False
        self.ps.registry_write()


class ChangeProxyL(ChangeProxy):

    def __init__(self, logger, ip, port):
        super().__init__(logger, ip, port)
        self.logger = logger
        self.ip = ip
        self.port = port
        self.new_str = [
            '############代理配置############\n',
            'export https_proxy="http://{0}:{1}"\n'.format(self.ip, self.port),
            'export http_proxy="http://{0}:{1}"\n'.format(self.ip, self.port),
            'export ftp_proxy="http://{0}:{1}"\n'.format(self.ip, self.port),
            '############代理配置############'
        ]
        self.file_path = "/etc/profile"

    def close_proxy(self):
        for ns in self.new_str:
            new_ns = ns.split("=")[0].split("\n")[0]
            os.system("sed -i '/{0}/d' {1}".format(new_ns, self.file_path))

    def set_proxy(self):
        self.close_proxy()
        with open(self.file_path, mode="a+", encoding="utf8") as f:
            f.writelines(self.new_str)


class ChangeProxyD(ChangeProxy):
    def close_proxy(self):
        pass

    def __init__(self, logger, ip, port):
        super().__init__(logger, ip, port)
        self.logger = logger
        self.ip = ip
        self.port = port

    def set_proxy(self):
        pip.main(['install', '--proxy', 'http://127.0.0.1:8080', 'mitmproxy'])
        pip.main(['install', '–-proxy', 'https://127.0.0.1:8080', 'mitmproxy'])
        pip.main(['install', '–-proxy', 'ftp://127.0.0.1:8080', 'mitmproxy'])


class ChangeProxyF(ChangeProxy):
    def close_proxy(self):
        pass

    def __init__(self, logger, ip, port):
        super().__init__(logger, ip, port)
        self.logger = logger
        self.ip = ip
        self.port = port

    def set_proxy(self):
        pip.main(['install', '--proxy', 'http://127.0.0.1:8080', 'mitmproxy'])
        pip.main(['install', '–-proxy', 'https://127.0.0.1:8080', 'mitmproxy'])
        pip.main(['install', '–-proxy', 'ftp://127.0.0.1:8080', 'mitmproxy'])


class RetProxy(ChangeProxy):
    def __init__(self, logger, ip, port):
        super().__init__(logger, ip, port)
        self.plat = platform.system()
        self.logger = logger
        self.ip = ip
        self.port = port

    def close_proxy(self):
        if self.plat == 'Windows':
            ChangeProxyW(self.logger, self.ip, self.port).close_proxy()
        elif self.plat == 'Darwin':
            ChangeProxyD(self.logger, self.ip, self.port).close_proxy()
        elif self.plat == 'Linux':
            ChangeProxyL(self.logger, self.ip, self.port).close_proxy()
        # elif self.plat == 'Linux':
        #     ChangeProxyL(self.logger, self.ip, self.port).close_proxy()
        elif self.plat == 'FreeBSD':
            ChangeProxyF(self.logger, self.ip, self.port).close_proxy()
        else:
            raise Exception("暂不支持设置该系统代理，请手动设置")
        self.logger.info("目前代理已关闭")

    def set_proxy(self):

        if self.plat == 'Windows':
            ChangeProxyW(self.logger, self.ip, self.port).set_proxy()
        elif self.plat == 'Darwin':
            ChangeProxyD(self.logger, self.ip, self.port).set_proxy()
        elif self.plat == 'Linux':
            ChangeProxyL(self.logger, self.ip, self.port).set_proxy()
        elif self.plat == 'FreeBSD':
            ChangeProxyF(self.logger, self.ip, self.port).set_proxy()
        else:
            raise Exception("暂不支持设置该系统代理，请手动设置")
        self.logger.info("开启代理成功，目前代理ip：{0}，port：{1}".format(self.ip, self.port))

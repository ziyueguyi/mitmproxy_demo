# -*- coding: utf-8 -*-
# @项目名称 :demo
# @文件名称 :start.py
# @作者名称 :sxzhang1
# @日期时间 :2024/1/23 14:42
# @文件介绍 :
"""
mitmproxy_url:https://docs.mitmproxy.org/stable/
mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
import asyncio

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

from script.change_proxy import ChangeProxy
from script.log import LoggerFile
from event_script.events_base import EventsBase


class EventStart:
    """
    监听主机包的启动类
    """

    def __init__(self):
        self.logger = LoggerFile(self.__class__.__name__, log_dir="log")
        self.addons = EventsBase(logger=self.logger).get_child_class()
        self.cp = ChangeProxy(self.logger)

    @staticmethod
    def get_option(ip, port) -> Options:
        """
        获取并对配置文件进行操作
        :return:配置文件对象
        """
        opts = Options(listen_host=ip, listen_port=port)
        return opts

    def run(self):
        """
        主入口
        :return:
        """
        ip, port = "127.0.0.1", 8888
        self.cp.ip, self.cp.port = ip, port
        self.cp.set_proxy()
        opt = self.get_option(ip, port)
        loop = asyncio.new_event_loop()
        m = DumpMaster(options=opt, loop=loop)
        m.addons.add(*self.addons)
        try:
            asyncio.run(m.run())
        except KeyboardInterrupt:
            m.shutdown()
        finally:
            self.cp.close_proxy()


if __name__ == '__main__':
    EventStart().run()

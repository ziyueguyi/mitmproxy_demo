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
import configparser
import queue

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

from event_script.events_base import EventsBase
from script.change_proxy import RetProxy
from script.log import Logger


class EventStart:
    """
    监听主机包的启动类
    """

    def __init__(self):
        self.setting = configparser.ConfigParser()
        self.setting.read("config.ini")
        self.ip = self.setting.get("main", "ip")
        self.port = int(self.setting.get("main", "port"))
        self.logger = Logger(self.__class__.__name__, log_dir=self.setting.get("main", "log_path"))
        self.logger.is_color = True
        self.logger.format = "[datetime] [[class_name]]|<[log_level]>|([lineno]):[message|extra]"
        self.logger.date_rotate = True
        self.queue = queue.Queue()
        self.addons = EventsBase(logger=self.logger, setting=self.setting, queue=self.queue).get_child_class()
        self.rp = RetProxy(self.logger, self.ip, self.port)

    def get_option(self) -> Options:
        """
        获取并对配置文件进行操作
        :return:配置文件对象
        """
        opts = Options(listen_host=self.ip, listen_port=self.port)
        return opts

    def run(self):
        """
        主入口
        :return:
        """
        self.rp.ip, self.rp.port = self.ip, self.port
        self.rp.set_proxy()
        opt = self.get_option()
        loop = asyncio.new_event_loop()
        m = DumpMaster(options=opt, loop=loop)
        m.addons.add(*self.addons)
        try:
            asyncio.run(m.run())
        except KeyboardInterrupt:
            m.shutdown()
        finally:
            self.rp.close_proxy()


if __name__ == '__main__':
    EventStart().run()

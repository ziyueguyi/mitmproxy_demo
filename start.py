# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :start.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog: https://www.wenjiangs.com/doc/6rzvlmcm
"""
import asyncio

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

from bases_tools import BasesTools
from events_base import EventsBase
from events_log import BaseLogger


class EventStart:
    """
    监听主机包的启动类
    """
    __instance = None

    def __new__(cls, *args, **kwargs):

        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        ignore_class = [
            "EventsQUIC",
            "EventsUDP",
            "EventsTCP",
            "EventsHttp",
            "EventsSockSv5",
            "EventsConnection",
            # "EventsTLS",
            "EventsWebSocket"
            "EventsDNS"
        ]
        self.logger = BaseLogger()
        EventsBase(logger=self.logger)
        self.bt = BasesTools()
        self.bt.ignore_class = ignore_class
        self.addons = self.bt.class_set

    @staticmethod
    def get_option() -> Options:
        """
        获取并对配置文件进行操作
        :return:配置文件对象
        """
        opts = Options(listen_host='127.0.0.1', listen_port=8080)
        return opts

    # def run(self):
    #     async def _main():
    #         options = Options(listen_host='127.0.0.1', listen_port=8080, mode=['upstream:https://localhost:8080'],
    #                           ssl_insecure=True)
    #
    #         m = DumpMaster(options=options)
    #
    #         m.server = Proxy_server()
    #         m.addons.add(*self.addons)
    #         await m.run()
    #
    #     try:
    #         print("开始抓取数据")
    #         asyncio.run(_main())
    #     except KeyboardInterrupt:
    #         pass
    #         print("结束啦")
    def run(self):
        """
        主入口
        :return:
        """
        self.logger.info("开始抓取数据啦，小心隐私被抓取")
        option = self.get_option()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        m = DumpMaster(option, loop=loop)
        m.addons.add(*self.addons)
        try:
            asyncio.run(m.run())
        except (KeyboardInterrupt, RuntimeError):
            m.shutdown()
        finally:
            self.logger.info("结束啦，不用担心咯!")


if __name__ == '__main__':
    EventStart().run()

# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :start.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
mitmproxy_url:https://docs.mitmproxy.org/stable/
mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
import asyncio

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster
from script.log import LoggerFile
from event_script.events_base import EventsBase


class EventStart:
    """
    监听主机包的启动类
    """

    def __init__(self):
        self.logger = LoggerFile(self.__class__.__name__, log_dir="log")
        self.addons = EventsBase(logger=self.logger).get_child_class()

    @staticmethod
    def get_option() -> Options:
        """
        获取并对配置文件进行操作
        :return:配置文件对象
        """
        opts = Options(listen_host='127.0.0.1', listen_port=8888)
        return opts

    @staticmethod
    async def update_config(flow):

        # 根据需要获取上游代理地址，并将其设置为 upstream_proxy 参数值
        # upstream_proxy = await get_upstream_proxy()
        # flow.options.upstream_proxy = upstream_proxy
        pass

    def run(self):
        """
        主入口
        :return:
        """
        self.logger.info("代理正在开启")
        opt = self.get_option()
        loop = asyncio.new_event_loop()
        m = DumpMaster(options=opt, loop=loop)
        m.addons.add(*self.addons)
        try:
            asyncio.run(m.run())
        except KeyboardInterrupt:
            m.shutdown()
        self.logger.info("代理正在关闭")


if __name__ == '__main__':
    EventStart().run()

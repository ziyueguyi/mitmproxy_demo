# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :events_socket_sv5.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
from mitmproxy.proxy import layers

from event_script.events_base import EventsBase


class EventsSockSv5(EventsBase):
    """
    socket在代理情况下，对数据进行捕获
    """

    def __init__(self, logger, setting, queue):
        super().__init__(logger=logger, setting=setting, queue=queue)

    @staticmethod
    def socks5_auth(data_flow: layers.modes.Socks5AuthData) -> None:
        """
        Mitmproxy has received username/password SOCKS5 credentials.
        This hook decides whether they are valid by setting data.valid.
        :param data_flow:
        :return:
        """
        pass

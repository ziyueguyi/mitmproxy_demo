# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :events_tcp.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
from mitmproxy import tcp

from events_base import EventsBase


class EventsTCP(EventsBase):
    """
    TCP连接，对数据包进行捕获
    """

    def __init__(self):
        super().__init__()

    def tcp_start(self, data_flow: tcp.TCPFlow) -> None:
        """
        A TCP connection has started.
        :param data_flow:
        :return:
        """
        self.logger.info("tcp++++++++++++++++++++++++++++++++++")

    def tcp_message(self, data_flow: tcp.TCPFlow) -> None:
        """
        A TCP connection has received a message. The most recent message will be flow. Messages[-1]. The message is
        user-modifiable.

        :param data_flow:
        :return:
        """
        self.logger.info("tcp++++++++++++++++++++++++++++++++++")

    def tcp_end(self, data_flow: tcp.TCPFlow) -> None:
        """
        A TCP connection has ended.
        :param data_flow:
        :return:
        """
        self.logger.info("tcp++++++++++++++++++++++++++++++++++")

    def tcp_error(self, data_flow: tcp.TCPFlow) -> None:
        """
        A TCP error has occurred.
        Every TCP flow will receive either a tcp_error or a tcp_end event, but not both.
        :param data_flow:
        :return:
        """
        self.logger.info("tcp++++++++++++++++++++++++++++++++++")

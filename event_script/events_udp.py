# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :events_udp.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
from mitmproxy import udp

from event_script.events_base import EventsBase


class EventsUDP(EventsBase):
    """
    UDP转发的情况下对数据包进行捕获
    """

    def __init__(self, logger, setting, queue):
        super().__init__(logger=logger, setting=setting, queue=queue)

    @staticmethod
    def udp_start(data_flow: udp.UDPFlow) -> None:
        """
        A UDP connection has started.
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def udp_message(data_flow: udp.UDPFlow) -> None:
        """
        A UDP connection has received a message. The most recent message will be flow. Messages[-1]. The message is
        user-modifiable.
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def udp_end(data_flow: udp.UDPFlow) -> None:
        """
        A UDP connection has ended.
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def udp_error(data_flow: udp.UDPFlow) -> None:
        """
        A UDP error has occurred.
        Every UDP flow will receive either a udp_error or a udp_end event, but not both.
        :param data_flow:
        :return:
        """
        pass

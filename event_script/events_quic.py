# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :events_quic.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
from mitmproxy.proxy import layers

from event_script.events_base import EventsBase


class EventsQUIC(EventsBase):
    """
    快速UDP转发的情况下对数据包进行捕获
    """

    def __init__(self, logger, setting):
        super().__init__(logger=logger, setting=setting)

    @staticmethod
    def quic_start_client(data_flow: layers.quic.QuicTlsData) -> None:
        """
        LS negotiation between mitmproxy and a client over QUIC is about to start.
        An addon is expected to initialize data.settings. (by default, this is done by mitmproxy.addons.tls config)
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def quic_start_server(data_flow: layers.quic.QuicTlsData) -> None:
        """
        TLS negotiation between mitmproxy and a server over QUIC is about to start.
        An addon is expected to initialize data.settings. (by default, this is done by mitmproxy.addons.tls config)
        :param data_flow:
        :return:
        """
        pass

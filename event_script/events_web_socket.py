# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :events_web_socket.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
from mitmproxy import http

from event_script.events_base import EventsBase


class EventsWebSocket(EventsBase):
    """
    socket连接的情况下，对双发发送数据进行捕获
    """

    def __init__(self, logger, setting):
        super().__init__(logger=logger, setting=setting)

    @staticmethod
    def websocket_start(data_flow: http.HTTPFlow) -> None:
        """
        A WebSocket connection has commenced.
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def websocket_message(data_flow: http.HTTPFlow) -> None:
        """
        Called when a WebSocket message is received from the client or server. The most recent message will be
        flow. Messages[-1]. The message is user-modifiable. Currently, there are two types of messages, corresponding
        to the BINARY and TEXT frame types.
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def websocket_end(data_flow: http.HTTPFlow) -> None:
        """
        A WebSocket connection has ended. You can check flow.websocket.close_code to determine why it ended.
        :param data_flow:
        :return:
        """
        pass

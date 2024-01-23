# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :events_connection.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
from mitmproxy import connection
from mitmproxy.proxy import server_hooks

from event_script.events_base import EventsBase


class EventsConnection(EventsBase):
    """
    网络连接生命周期类
    """

    def __init__(self, logger, setting):
        super().__init__(logger=logger, setting=setting)

    @staticmethod
    def client_connected(data_flow: connection.Client) -> None:
        """
        A client has connected to mitmproxy. Note that a connection can correspond to multiple HTTP requests.
        Setting client. Error kills the connection.
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def client_disconnected(data_flow: connection.Client) -> None:
        """
        A client connection has been closed (either by us or the client).
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def server_connect(data_flow: server_hooks.ServerConnectionHookData) -> None:
        """
        Mitmproxy is about to connect to a server. Note that a connection can correspond to multiple requests.
        Setting data.server.error kills the connection.
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def server_connected(data_flow: server_hooks.ServerConnectionHookData) -> None:
        """
        Mitmproxy has connected to a server.
        :param data_flow:
        :return:
        """
        pass

    @staticmethod
    def server_disconnected(data_flow: server_hooks.ServerConnectionHookData) -> None:
        """
        A server connection has been closed (either by us or the server).
        :param data_flow:
        :return:
        """
        pass

# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :mitmproxy.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
from mitmproxy import tls

from event_script.events_base import EventsBase


class EventsTLS(EventsBase):
    """
    TLS握手的情况下对握手数据进行接收
    """

    def __init__(self, logger, setting, queue):
        super().__init__(logger=logger, setting=setting, queue=queue)

    @staticmethod
    def tls_client_hello(data_flow: tls.ClientHelloData) -> None:
        """
        Mitmproxy has received a TLS ClientHello message. This hook decides whether a server connection is needed to
        negotiate TLS with the client (data.establish_server_tls_first)

        :param data_flow:
        :return:
        """
        print("TLS", data_flow)

    @staticmethod
    def tls_start_client(data_flow: tls.TlsData) -> None:
        """
        TLS negotiation between mitmproxy and a client is about to start.
        An addon is expected to initialize data.ssl_conn. (by default, this is done by mitmproxy.addons.tls config)
        :param data_flow:
        :return:
        """
        print("TLS", data_flow)

    @staticmethod
    def tls_start_server(data_flow: tls.TlsData) -> None:
        """
        TLS negotiation between mitmproxy and a server is about to start.
        An addon is expected to initialize data.ssl_conn. (by default, this is done by mitmproxy.addons.tls config)
        :param data_flow:
        :return:
        """
        print("TLS", data_flow)

    @staticmethod
    def tls_established_client(data_flow: tls.TlsData) -> None:
        """
        The TLS handshake with the client has been completed successfully.
        :param data_flow:
        :return:
        """
        print("TLS", data_flow)

    @staticmethod
    def tls_established_server(data_flow: tls.TlsData) -> None:
        """
        The TLS handshake with the server has been completed successfully.
        :param data_flow:
        :return:
        """
        print("TLS", data_flow)

    @staticmethod
    def tls_failed_client(data_flow: tls.TlsData) -> None:
        """
        The TLS handshake with the client has failed.
        :param data_flow:
        :return:
        """
        print("TLS", data_flow)

    @staticmethod
    def tls_failed_server(data_flow: tls.TlsData) -> None:
        """
        The TLS handshake with the server has failed.
        :param data_flow:
        :return:
        """
        print("TLS", data_flow)

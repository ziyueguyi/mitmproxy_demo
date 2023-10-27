# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :events_dns.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
from mitmproxy import dns

from events_base import EventsBase


class EventsDNS(EventsBase):
    """
    获取DNS解析数据类
    """

    def __init__(self):
        super().__init__()

    def dns_request(self, data_flow: dns.DNSFlow) -> None:
        """
        A DNS query has been received.
        :param data_flow:
        :return:
        """
        self.logger.info("DNS++++++++++++++++++++++++++++++++++")

    def dns_response(self, data_flow: dns.DNSFlow) -> None:
        """
        A DNS response has been received or set.
        :param data_flow:
        :return:
        """
        self.logger.info("DNS++++++++++++++++++++++++++++++++++")

    def dns_error(self, data_flow: dns.DNSFlow) -> None:
        """
        A DNS error has occurred.
        :param data_flow:
        :return:
        """
        self.logger.info("DNS++++++++++++++++++++++++++++++++++")

# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :events_base.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
from urllib.parse import urljoin

from mitmproxy import http
from events_base import EventsBase


class EventsHttp(EventsBase):
    """
    http请求数据包进行捕获
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    @EventsBase.add_star
    def request_headers(data_flow: http.HTTPFlow) -> None:
        """
        已成功读取HTTP请求标头。此时，身体是空的。
        :param data_flow:
        :return:
        """
        print("http:请求头：{0}", data_flow.request.headers.items(), end="\n")

    @staticmethod
    @EventsBase.add_star
    def request(data_flow: http.HTTPFlow) -> None:
        """
        已读取完整的HTTP请求。注意：如果请求流处于活动状态，则在整个
        尸体已被流式传输。HTTP尾部（如果存在）尚未传输到服务器，并且仍然可以
        修改。启用流可能会导致意外的事件序列：例如，现在可能会发生响应
        因为服务器在上传过程中回复“413 Payload Too Large”。
        :param data_flow:请求数据流
        :return:None
        """
        data = data_flow.request.data
        print("请求协议：", data.http_version.decode(), end="\n")
        print("请求网址：{0}://{1}".format(data.scheme.decode(), data.host), end="\n")
        assert data.port in [80, 443]
        print("请求端口：{0}({1})".format("HTTP请求" if data.port == 80 else "HTTPS请求", data.port), end="\n")
        print("请求方法：", data.method.decode(), end="\n")

    @staticmethod
    @EventsBase.add_star
    def response_headers(data_flow: http.HTTPFlow) -> None:
        """
        已成功读取HTTP响应标头。此时，身体是空的。
        :param data_flow:
        :return:
        """
        print("https:请求头：", data_flow.request.headers.items(), end="\n")

    @staticmethod
    @EventsBase.add_star
    def response(data_flow: http.HTTPFlow) -> None:
        """
        已读取完整的HTTP响应。注意：如果响应流处于活动状态，则在
        整个身体都流了出来。HTTP预告片（如果存在）尚未传输到客户端，可以
        仍有待修改。
        :param data_flow:
        :return:
        """
        print("状态码：", data_flow.response.data.status_code, end="\n")
        print("协议码：", data_flow.response.data.http_version.decode().strip(), end="\n")
        print("响应体：", data_flow.response.data.content.decode().strip(), end="\n")

    @staticmethod
    @EventsBase.add_star
    def error(data_flow: http.HTTPFlow) -> None:
        """
        出现HTTP错误，例如服务器响应无效或连接中断。这与
        一个有效的服务器HTTP错误响应，它只是一个带有HTTP错误代码的响应。每个流量
        接收错误或响应事件，但不能同时接收两者。
        :param data_flow:
        :return:
        """
        print(data_flow.request)

    @staticmethod
    @EventsBase.add_star
    def http_connect(data_flow: http.HTTPFlow) -> None:
        """
        收到HTTP 连接请求。出于大多数实际目的，可以忽略此事件。仅此事件
        当客户端指示mitmproxy打开与上游主机。在流上设置非2xx响应将向客户端返回响应并中止
        联系连接请求是针对mitmproxy本身的HTTP代理指令，不会转发。他们没有
        生成通常的HTTP处理程序事件，但所有通过新打开的连接的请求都会。
        :param  data_flow:
        :return:
        """
        print("连接id：", data_flow.id, end="\n")

    @staticmethod
    @EventsBase.add_star
    def http_connect_upstream(data_flow: http.HTTPFlow) -> None:
        """
        HTTP 连接请求即将发送到上游代理。大多数情况下可以忽略此事件
        实际目的。此事件可用于设置上游代理的自定义身份验证标头。连接
        请求不会生成通常的HTTP处理程序事件，但所有通过新打开的请求
        连接将。
        :param data_flow:
        :return:
        """
        print("https:请求头：", data_flow.get_state(), end="\n")

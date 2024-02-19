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
from mitmproxy import http

from event_script.events_base import EventsBase


class EventsHttp(EventsBase):
    """
    http请求数据包进行捕获
    """

    def __init__(self, logger, setting, queue):
        super().__init__(logger=logger, setting=setting, queue=queue)

    @staticmethod
    def request_headers(data_flow: http.HTTPFlow) -> None:
        """
        HTTP request headers were successfully read. At this point, the body is empty.
        :param data_flow:
        :return:
        """
        print("访问1：", data_flow.request.headers)

    @staticmethod
    def request(data_flow: http.HTTPFlow) -> None:
        """
        The full HTTP request has been read. Note: If request streaming is active, this event fires after the entire
        body has been streamed. HTTP trailers, if present, have not been transmitted to the server yet and can still
        be modified. Enabling streaming may cause unexpected event sequences: For example, response may now occur
        before request because the server replied with "413 Payload Too Large" during upload.
        :param data_flow:
        :return:
        """
        print("访问2：", data_flow.request)

    @staticmethod
    def response_headers(data_flow: http.HTTPFlow) -> None:
        """
        HTTP response headers were successfully read. At this point, the body is empty.
        :param data_flow:
        :return:
        """
        print("访问3：", data_flow.request)

    @staticmethod
    def response(data_flow: http.HTTPFlow) -> None:
        """
        The full HTTP response has been read. Note: If response streaming is active, this event fires after the
        entire body has been streamed. HTTP trailers, if present, have not been transmitted to the client yet and can
        still be modified.



        :param data_flow:
        :return:
        """
        print("访问4：", data_flow.request)

    @staticmethod
    def error(data_flow: http.HTTPFlow) -> None:
        """
        An HTTP error has occurred, e.g. invalid server responses, or interrupted connections. This is distinct from
        a valid server HTTP error response, which is simply a response with an HTTP error code. Every flow will
        receive either an error or a response event, but not both.
        :param data_flow:
        :return:
        """
        print("访问5：", data_flow.request)

    @staticmethod
    def http_connect(data_flow: http.HTTPFlow) -> None:
        """
        An HTTP CONNECT request was received. This event can be ignored for most practical purposes. This event only
        occurs in regular and upstream proxy modes when the client instructs mitmproxy to open a connection to an
        upstream host. Setting a non 2xx response on the flow will return the response to the client and abort the
        connection. CONNECT requests are HTTP proxy instructions for mitmproxy itself and not forwarded. They do not
        generate the usual HTTP handler events, but all requests going over the newly opened connection will.
        :param  data_flow:
        :return:
        """
        print("访问6：", data_flow.request)

    @staticmethod
    def http_connect_upstream(data_flow: http.HTTPFlow) -> None:
        """
        An HTTP CONNECT request is about to be sent to an upstream proxy. This event can be ignored for most
        practical purposes. This event can be used to set custom authentication headers for upstream proxies. CONNECT
        requests do not generate the usual HTTP handler events, but all requests going over the newly opened
        connection will.
        :param data_flow:
        :return:
        """
        print("访问7：", data_flow.request)
